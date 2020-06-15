import PySimpleGUI as sg
import yagmail
import sys
import rsa

#Кнопка отправть
def sendMailButton():
  #Выбор алгоритма
  SelectorLayout = [
            [sg.Text("Шифрование алгоритмом:", justification='center', auto_size_text = False)],
            [sg.Radio('RSA', 'ciphers', default=True)],
            [sg.Button('Дальше'), sg.Button('Домой'), sg.Button('Выйти')]
            ]

  RSALayout = [
          [sg.Text('Введите информацию!', auto_size_text=False, justification='left', font=('Helvetica', 20))],
          [sg.Text('Ваш E-Mail адрес', size=(20, 1)), sg.InputText()],
          [sg.Text('Ваш пароль', size=(20, 1)), sg.InputText(password_char='*')],
          [sg.Text('Кому отправить сообщение?', size=(20,1)), sg.InputText()],
          [sg.Text('Тема (не шифруется)', size=(20,1)), sg.InputText()],
          [sg.Text('Ваше письмо:', size=(20, 1)), sg.Multiline(size=(45,5), autoscroll=True, background_color='grey')],
          [sg.Text('Открытый ключ:', size=(20, 1)), sg.Output(size=(45,5))],
          [sg.ReadButton('Отправить сообщение',font=('Helvetica',13), auto_size_button=True, bind_return_key=True),
          sg.ReadButton('Отправить открытый ключ', font=('Helvetica', 13), auto_size_button=True, bind_return_key=True),
          sg.ReadButton('Сгенерировать ключ', font=('Helvetica', 13), auto_size_button=True),
          sg.FileBrowse('Выбрать открытый ключ', font=('Helvetica', 13)),
          sg.Button('Домой',font=('Helvetica',13), auto_size_button=True),
          sg.ReadButton('Выйти',font=('Helvetica',13), auto_size_button=True)]
            ]
  #Что видит пользователь
  window = sg.Window('emailEncryptor').Layout(RSALayout)
  window2 = sg.Window('Выбор алгоритма:').Layout(SelectorLayout)
  # Отправка сообщения и генерация
  while True:
    button, values = window2.Read()
    if button == 'Дальше':
        if values[0] == True:
            window2.hide()
            button3, values3 = window.Read()
            if button3 == 'Сгенерировать ключ':
                (pubkey, privkey) = rsa.newkeys(512)
                privkey_pem = privkey.save_pkcs1()
                pubkey_pem = pubkey.save_pkcs1()
                print(pubkey)
                # запись открытого ключа в файл
                f = open('pubkey.pem', mode='wb')
                f.write(pubkey_pem)
                f.close()

                # запись закрытого ключа в файл
                f = open('privkey.pem', mode='wb')
                f.write(privkey_pem)
                f.close()
            button2, values2 = window.Read()
            if button2 == 'Отправить открытый ключ':
                yag = yagmail.SMTP(values2[0], values2[1])
                yag.send(values2[2], values2[3], 'pubkey.pem')
                sg.Popup('Ключ успешно отправлен!')
            if button2 == 'Отправить сообщение':
                     # запись открытого клбюча из файла
                     with open('pubkey.pem', mode='rb') as publicfile:
                          keydata = publicfile.read()
                     keyencrypt = rsa.PublicKey.load_pkcs1(keydata)

                     # зашифрованный текст
                     encryptedContent = rsa.encrypt(values2[4].encode('utf8'), keyencrypt)
                     # отправка сообщения
                     f = open('Encrypt.txt', mode='wb')
                     f.write(encryptedContent)
                     f.close()


                     yag = yagmail.SMTP(values2[0], values2[1])
                     yag.send(values2[2], values2[3], 'Encrypt.txt')
                     sg.Popup('Сообщение успешно отправлено!')

            if button2 == 'Домой':
                      window.Hide()
                      home()
            else:
               sys.exit()

#Кнопка "расшифровать"
def decodeMailButton():

  #Выбор алгоритма шифрования


  DecryptSelector = [
            [sg.Text("Расшифрование методом:", justification='center', auto_size_text = False)],
            [sg.Radio('RSA', 'ciphers', default=True)],
            [sg.Button('Дальше', bind_return_key=True), sg.Button('Домой'), sg.Button('Выйти')]
            ]

  RSALayout = [
      [sg.Text('Ваше зашифрованное сообщение:'), sg.InputText(do_not_clear=True, size=(15,2))],
      [sg.ReadButton('Расшифровать',font=('Helvetica',15), auto_size_button=True, bind_return_key=True),
      sg.FileBrowse('Выбрать зашифрованное сообщение', font=('Helvetica', 15)),
      sg.Button('Домой', font=('Helvetica',15), auto_size_button=True),
      sg.Exit(font=('Helvetica',15), auto_size_button=True)]
      ]

  #Что видит пользователь
  window = sg.Window('emailEncryptor').Layout(DecryptSelector)
  window2 = sg.Window('emailEncryptor').Layout(RSALayout)

  while True:
    button, values = window.Read()
    if button == 'Дальше':
      if values[0] == True:
        window.Hide()
        button2, values2 = window2.Read()
        if button2 == 'Расшифровать':

            #ключ для расшифровки


            with open('privkey.pem', mode='rb') as privatefile:
                keydata = privatefile.read()
            keydecrypt = rsa.PrivateKey.load_pkcs1(keydata)
            #выбор файла для расшифровки

            f = open('Encrypt.txt', mode='rb')
            EncryptTEXT = f.read()
            f.close()

            decodedContent = rsa.decrypt(EncryptTEXT, keydecrypt)
            decodedContentNOTUTF = decodedContent.decode('utf8')
            window2.Hide()
            displayMessage(decodedContentNOTUTF)

        elif button2 == 'Домой':
          window2.Hide()
          home()
        else:
          sys.exit()

#Сообщение после расшифровки
def displayMessage(string):
  # Layout design
  layout = [
        [sg.Multiline(string, size=(55,20), auto_size_text=True)],
        [sg.Text(''), sg.Button('Назад', auto_size_button=True)]]

  window = sg.Window('Зашифрованное сообщение:').Layout(layout)
  while True:
    button, values = window.Read()
    if button == 'Назад':
      window.Hide()
      decodeMailButton()
    else:
      break

# Кнопка домой
def home():

  # кастомизация
  sg.SetOptions(scrollbar_color=None,
           button_color=('white','#475841'),
           font=('Helvetica', 20),
           input_elements_background_color='#F7F3EC')

  # дизайн домашнего окна
  layout = [[sg.Text('Приложение для передачи защищённого сообщения по email', size=(45,2), justification='center', font=('Helvetica', 20))],
           [sg.Text('')],
           [sg.Text('Разработано Романом Износовым', auto_size_text=False, justification='center', font=('Helvetica', 20))],
           [sg.Text('')],
           [sg.Text('',size=(11,1)),
            sg.Button('Отправить', font = ('Helvetica',15), auto_size_button=True),
            sg.Button('Расшифровать', font=('Helvetica',15), auto_size_button=True),
            sg.Quit('Выйти',font=('Helvetica',15),auto_size_button=True)]]

  window = sg.Window('RSA emailEncryptor').Layout(layout)

  # Главное меню
  while True:
    # Read the Window
    button, value = window.Read()
    # Take appropriate action based on button
    if button == 'Отправить':
          window.Hide()
          sendMailButton()
    elif button == 'Расшифровать':
        window.Hide()
        decodeMailButton()
    elif button =='Выйти' or button is None:
        sys.exit()
    break
home()