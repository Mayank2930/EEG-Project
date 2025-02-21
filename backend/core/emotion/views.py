import base64
from io import BytesIO
from PIL import Image
import cv2
import numpy as np
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from emotion.utils.emotion import detect_emotion_from_frame
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.permissions import AllowAny
import os
from .utils.eeg_preprocess import model
from .serializers import EEGFeaturesSerializer
from .serializers import EEGSignalSerializer
from .utils.arduino import send_to_arduino
import serial
import time
from datetime import datetime
from .models import EEGSignal   

FEATURE_NAMES = [
    "Mean", "Max", "Standard_Deviation", "RMS", "Peak_to_Peak", "Abs_Diff_Signal", "Alpha_Power"
]

SERIAL_PORT = 'COM8'
BAUD_RATE = 9600

class AlphaPowerView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Store EEG signal data in the database.
        """
        # Add the timestamp to the request data
        data_with_timestamp = {
            **request.data,
            "timestamp": datetime.now()
        }

        # Use EEGSignalSerializer to save the data
        serializer = EEGSignalSerializer(data=data_with_timestamp)
        if serializer.is_valid():
            try:
                serializer.save()  # Save the validated data to the database
                return Response({"message": "Data stored successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        Retrieve the last 5 EEG signals for plotting.
        """
        signals = EEGSignal.objects.all().order_by('-timestamp')[:5]
        data = [
        {
            "timestamp": signal.timestamp,      # Model field
            "alpha_power": signal.Alpha_Power,  # Model field
            "mean": signal.Mean,               # Model field
            "max": signal.Max,                 # Model field
        }
            for signal in signals
        ]
        return Response(data, status=status.HTTP_200_OK)

class DetectEmotionView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            frame_data = request.data.get('frame')
            if not frame_data:
                return Response({"error": "No frame data provided"}, status=status.HTTP_400_BAD_REQUEST)

            frame_data = frame_data.split(',')[1]  
            img_bytes = base64.b64decode(frame_data)
            img = Image.open(BytesIO(img_bytes))

            frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

            results = detect_emotion_from_frame(frame)
            return Response({"emotions": results}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        

class PredictMovementView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Initialize Wired Serial Communication
        try:
            # Replace the Bluetooth port with your wired serial port (e.g., COM3, /dev/ttyUSB0)
            serial_connection = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            print(f"Serial communication established on {SERIAL_PORT}")
            time.sleep(2)  # Add delay to ensure the serial connection is ready

        except serial.SerialException as e:
            return Response({
                'error': f"Failed to open serial port {SERIAL_PORT}: {e}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = EEGFeaturesSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Prepare features for prediction
                features = pd.DataFrame([[
                    serializer.validated_data['Mean'],
                    serializer.validated_data['Max'],
                    serializer.validated_data['Standard_Deviation'],
                    serializer.validated_data['RMS'],
                    serializer.validated_data['Peak_to_Peak'],
                    serializer.validated_data['Abs_Diff_Signal'],
                    serializer.validated_data['Alpha_Power'],
                ]])

                # Perform prediction
                prediction = model.predict(features)[0]
                print(f"Prediction: {prediction}")

                # Send prediction to the device via wired serial communication
                message = f"{prediction}\n"  # Append newline for Arduino
                serial_connection.write(message.encode('utf-8'))
                serial_connection.flush()
                time.sleep(1)  # Add delay after sending to ensure the device processes it
                print(f"Sent via Serial: {message}")

                # Return response to client
                return Response({'movement': prediction}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({
                    'error': f"Prediction failed: {str(e)}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            finally:
                if serial_connection and serial_connection.is_open:
                    serial_connection.close()
                    print("Serial connection closed.")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class EEGFeatureExtractionView(APIView):
#     parser_classes = [MultiPartParser, FormParser]
#     permission_classes = [AllowAny]

#     def post(self, request, format=None):
#         set_file = request.FILES.get('set_file', None)
#         fdt_file = request.FILES.get('fdt_file', None)

#         if not set_file or not fdt_file:
#             return Response({'error': 'Both .set and .fdt files must be uploaded'}, status=status.HTTP_400_BAD_REQUEST)

#         upload_dir = "uploads"
#         os.makedirs(upload_dir, exist_ok=True)

#         set_file_path = os.path.join(upload_dir, set_file.name)
#         fdt_file_path = os.path.join(upload_dir, set_file.name.replace('.set', '.fdt'))

#         with open(set_file_path, 'wb') as f:
#             for chunk in set_file.chunks():
#                 f.write(chunk)

#         with open(fdt_file_path, 'wb') as f:
#             for chunk in fdt_file.chunks():
#                 f.write(chunk)

#         try:
#             data, sfreq = load_eeg(set_file_path)

#             features = extract_features(data, sfreq)

#             os.remove(set_file_path)
#             os.remove(fdt_file_path)

#             return Response(features, status=status.HTTP_200_OK)
#         except Exception as e:
#             if os.path.exists(set_file_path):
#                 os.remove(set_file_path)
#             if os.path.exists(fdt_file_path):
#                 os.remove(fdt_file_path)
#             return Response({'error': f"Error loading EEG data: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class PredictMovementView(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         serializer = EEGFeaturesSerializer(data=request.data)
#         if serializer.is_valid():
#             features = np.array([[
#                 serializer.validated_data['Mean'],
#                 serializer.validated_data['Max'],
#                 serializer.validated_data['Standard_Deviation'],
#                 serializer.validated_data['RMS'],
#                 serializer.validated_data['Kurtosis'],
#                 serializer.validated_data['Skewness'],
#                 serializer.validated_data['Alpha_Power'],
#             ]])
#             prediction = model.predict(features)[0]
#             try:
#                 with serial.Serial(BLUETOOTH_PORT, BAUD_RATE, timeout=1) as bluetooth:
#                     bluetooth.write(str(prediction).encode())  # Send prediction as string
#             except serial.SerialException as e:
#                 return Response({'movement': prediction,'error': f'Bluetooth communication failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#             # Return response to client
#             return Response({'movement': prediction}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class PredictMovementView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = EEGFeaturesSerializer(data=request.data)
#         if serializer.is_valid():
#             features = np.array([[
#                 serializer.validated_data['Mean'],
#                 serializer.validated_data['Max'],
#                 serializer.validated_data['Standard_Deviation'],
#                 serializer.validated_data['RMS'],
#                 serializer.validated_data['Kurtosis'],
#                 serializer.validated_data['Skewness'],
#                 serializer.validated_data['Alpha_Power'],
#             ]])
#             # Get the prediction
#             prediction = model.predict(features)[0]

#             # Send the movement command to Arduino
#             result = send_to_arduino(prediction)
#             if result is True:
#                 return Response(
#                     {'movement': prediction, 'message': 'Command sent to Arduino via Wi-Fi.'},
#                     status=status.HTTP_200_OK
#                 )
#             else:
#                 return Response(
#                     {'movement': prediction, 'error': f'Failed to send command via Wi-Fi: {result}'},
#                     status=status.HTTP_500_INTERNAL_SERVER_ERROR
#                 )

#         # Return errors if validation fails
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

