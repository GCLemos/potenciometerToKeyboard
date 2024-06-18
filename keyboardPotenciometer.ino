const int potPin = A2;   // Pino onde o potenciômetro está conectado
int lastValue = 0;       // Variável para armazenar o último valor lido do potenciômetro
int threshold = 10;      // Limite de variação para considerar uma mudança significativa

void setup() {
  Serial.begin(9600);    // Iniciar a comunicação serial
}

void loop() {
  int potValue = analogRead(potPin);              // Ler o valor do potenciômetro
  int mappedValue = map(potValue, 0, 1023, 0, 255); // Mapear o valor para a faixa de 0 a 255

  if (abs(mappedValue - lastValue) > threshold) {  // Verificar se a mudança é significativa
    if (mappedValue > lastValue) {  // Incremento
      Serial.println("RIGHT");
    } else if (mappedValue < lastValue) {  // Decremento
      Serial.println("LEFT");
    }
    
    lastValue = mappedValue;  // Atualizar o último valor
  }

  delay(100); // Pequeno atraso para estabilidade
}
