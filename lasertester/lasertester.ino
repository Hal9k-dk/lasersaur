const int H_PIN = 3; // PWM support
const int L_PIN = 2;
const int WP_PIN = 1;
const int STEP = 5;

void setup()
{
    Serial.begin(115200);
    Serial.println("LaserTester v 0.1");

    pinMode(H_PIN, OUTPUT);
    pinMode(L_PIN, OUTPUT);
    pinMode(WP_PIN, OUTPUT);

    digitalWrite(H_PIN, 0);
    digitalWrite(L_PIN, 1);
    digitalWrite(WP_PIN, 0);
}

int l_state = 1;
int h_state = 0;
int wp_state = 0;
int pwm_on = 0;
int pwm_value = 0;

void process(char c)
{
    switch (c)
    {
    case 'l':
    case 'L':
        l_state = !l_state;
        digitalWrite(L_PIN, l_state);
        Serial.print("L set to ");
        Serial.println(l_state);
        break;

    case 'h':
    case 'H':
        h_state = !h_state;
        digitalWrite(H_PIN, h_state);
        Serial.print("H set to ");
        Serial.println(h_state);
        break;

    case 'w':
    case 'W':
        wp_state = !wp_state;
        digitalWrite(WP_PIN, wp_state);
        Serial.print("WP set to ");
        Serial.println(wp_state);
        break;

    case 'P':
    case 'p':
        pwm_on = !pwm_on;
        Serial.print("PWM ");
        Serial.println(pwm_on ? "on" : "off");
        pwm_value = 0;
        h_state = 0;
        digitalWrite(H_PIN, 0);
        break;

    case '+':
        pwm_value += STEP;
        if (pwm_value >= 255)
            pwm_value = 255;
        analogWrite(H_PIN, pwm_value);
        Serial.print("PWM set to ");
        Serial.println(pwm_value);
        break;

    case '-':
        pwm_value -= STEP;
        if (pwm_value < 0)
            pwm_value = 0;
        analogWrite(H_PIN, pwm_value);
        Serial.print("PWM set to ");
        Serial.println(pwm_value);
        break;

    case '?':
        Serial.println("Commands:\r\n"
                       "l\t\t"            "Toggle L\r\n"
                       "h\t\t"            "Toggle H\r\n"
                       "w\t\t"            "Toggle WP\r\n"
                       "p\t"              "Toggle PWM on H\r\n"
                       "+\t\t"            "Increase PWM value\r\n"
                       "-\t\t"            "Decrease PWM value");
        break;
        
    default:
        Serial.println("ERROR: Unknown command");
        break;
    }
}

void loop()
{
    if (Serial.available())
    {
       // Command from PC
       char c = Serial.read();
       process(c);
    }
    
    delay(10);
}
