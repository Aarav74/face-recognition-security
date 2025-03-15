#define trigPin 9     // Pin for ultrasonic sensor trigger
#define echoPin 10    // Pin for ultrasonic sensor echo
#define redLed 8      // Pin for red LED
#define greenLed 5    // Pin for green LED (updated to pin 5)
#define buzzer 6      // Pin for buzzer

unsigned long buzzerStartTime = 0;  // Variable to store the start time of the buzzer
bool buzzerActive = false;          // Flag to track if the buzzer is active

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Set pin modes
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(redLed, OUTPUT);
  pinMode(greenLed, OUTPUT);  // Updated to pin 5
  pinMode(buzzer, OUTPUT);
}

void loop() {
  // Measure distance using ultrasonic sensor
  long duration, distance;
  
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  duration = pulseIn(echoPin, HIGH);
  distance = (duration / 2) / 29.1; // Convert to cm
  
  // Send distance to Python script
  Serial.println(distance);

  // Check for commands from Python script
  if (Serial.available() > 0) {
    char command = Serial.read();  // Read command from Python script

    if (command == 'R') {
      // Wrong face detected: blink red LED and activate buzzer
      digitalWrite(greenLed, LOW);  // Turn off green LED
      digitalWrite(redLed, HIGH);   // Turn on red LED
      tone(buzzer, 1000);           // Activate buzzer (1 kHz tone)
      buzzerStartTime = millis();   // Record the start time of the buzzer
      buzzerActive = true;          // Set buzzer active flag
    } else if (command == 'G') {
      // Correct face detected: turn on green LED
      digitalWrite(redLed, LOW);    // Turn off red LED
      noTone(buzzer);               // Turn off buzzer
      digitalWrite(greenLed, HIGH); // Turn on green LED (updated to pin 5)
      buzzerActive = false;         // Reset buzzer active flag
    } else if (command == 'O') {
      // Reset: turn off all LEDs and buzzer
      digitalWrite(redLed, LOW);
      digitalWrite(greenLed, LOW);  // Updated to pin 5
      noTone(buzzer);
      buzzerActive = false;         // Reset buzzer active flag
    }
  }

  // Stop the buzzer after 10 seconds
  if (buzzerActive && (millis() - buzzerStartTime >= 10000)) {
    noTone(buzzer);               // Turn off buzzer
    digitalWrite(redLed, LOW);    // Turn off red LED
    buzzerActive = false;         // Reset buzzer active flag
  }

  delay(500); // Adjust delay as needed
}
