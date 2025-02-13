const int H_PIN = 3; // PWM support
const int L_PIN = 2;
const int WP_PIN = 1;

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

int get_int(const char* buffer, int len, int* next = nullptr)
{
    int index = 0;
    while (buffer[index] && isspace(buffer[index]) && len)
    {
        ++index;
        --len;
    }
    while (buffer[index] && !isspace(buffer[index]) && len)
    {
        ++index;
        --len;
    }
    const int BS = 30;
    if (index >= BS)
    {
        Serial.println("ERROR: Integer too long");
        return -1;
    }
    char intbuf[BS];
    memcpy(intbuf, buffer, index);
    intbuf[index] = 0;
    if (next)
        *next = index+1;
    return atoi(intbuf);
}

int index = 0;
const int BUF_SIZE = 200;
char buffer[BUF_SIZE];

int l_state = 1;
int h_state = 0;
int wp_state = 0;
int pwm_on = 0;
int pwm_value = 0;

void process(const char* buffer)
{
    switch (buffer[0])
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
        if (pwm_value < 255)
            ++pwm_value;
        analogWrite(H_PIN, pwm_value);
        Serial.print("PWM set to ");
        Serial.println(pwm_value);
        break;

    case '-':
        if (pwm_value >= 0)
            --pwm_value;
        analogWrite(H_PIN, pwm_value);
        Serial.print("PWM set to ");
        Serial.println(pwm_value);
        break;

    case 'h':
    case 'H':
        Serial.println("Commands:\r\n"
                       "p <idx>\t\t"            "Play sound\r\n"
                       "v <vol>\t\t"            "Set volume\r\n"
                       "o <idx> <val>\t"        "Set PWM output\r\n"
                       "s\t\t"                    "Stop sound");
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
       if ((c == '\r') || (c == '\n'))
       {
           buffer[index] = 0;
           index = 0;
           process(buffer);
       }
       else
       {
           if (index >= BUF_SIZE)
           {
               Serial.println("Error: Line too long");
               index = 0;
               return;
           }
           buffer[index++] = c;
       }
    }
    
    delay(10);
}
