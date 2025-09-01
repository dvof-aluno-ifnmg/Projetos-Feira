import cv2
import mediapipe as mp
import numpy as np
import math
import serial
arduino = serial.Serial('COM7', 9600, timeout=1)
def calculate_angle_3d(a, b, c):
    """
    Calcula o ângulo entre 3 pontos 3D (em graus).
    O ângulo é calculado na articulação 'b'.

    Args:
        a: Coordenadas do ponto A (ex: ombro) como um array numpy [x, y, z].
        b: Coordenadas do ponto B (ex: cotovelo) como um array numpy [x, y, z].
        c: Coordenadas do ponto C (ex: pulso) como um array numpy [x, y, z].

    Returns:
        O ângulo em graus (entre 0 e 180).
    """
    # 1. Criar os vetores
    # Vetor BA (de B para A)
    vec_ba = a - b
    # Vetor BC (de B para C)
    vec_bc = c - b

    # 2. Calcular o produto escalar
    dot_product = np.dot(vec_ba, vec_bc)

    # 3. Calcular as magnitudes (normas) dos vetores
    norm_ba = np.linalg.norm(vec_ba)
    norm_bc = np.linalg.norm(vec_bc)
    
    # Prevenção de divisão por zero
    if norm_ba == 0 or norm_bc == 0:
        return 0.0

    # 4. Calcular o cosseno do ângulo
    cos_angle = dot_product / (norm_ba * norm_bc)
    
    # 5. Clamp o valor para evitar erros de domínio no acos devido a imprecisões de ponto flutuante
    cos_angle = np.clip(cos_angle, -1.0, 1.0)

    # 6. Calcular o ângulo em radianos e converter para graus
    angle_rad = math.acos(cos_angle)
    angle_deg = math.degrees(angle_rad)

    return angle_deg

# Inicializa MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp.solutions.pose.Pose()
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture("http://192.168.1.104:4747/video")
angle=0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Converte para RGB (MediaPipe usa RGB, não BGR)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb) #define a variável results como o processamento de mp.solutions.pose, que é definido como pose
    if results.pose_world_landmarks:
        landmarks = results.pose_world_landmarks.landmark #retorna uma lista com os 33 objetos do landmark
        l_shoulder = np.array([landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z])
        l_elbow = np.array([landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].z])
        l_wrist = np.array([landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].z])
        angle = int(calculate_angle_3d(l_shoulder, l_elbow, l_wrist))
    print(angle)
    arduino.write(f"{angle}\n".encode())
    mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    cv2.imshow("Pose Detection", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC para sair
        break

cap.release()
cv2.destroyAllWindows()