# MyManager 🛡

## Why ❓
➡ manage all my accounts (websites, games, ...)  
➡ quickly copy/paste account  
➡ safely encrypt password  

## How to launch 🚀
Simply run `main.py`

## Todo ⏳
- [ ] Create template files (functions, classes, variables...)
- [ ] List every security related case
- [ ] Choose every algorithm needed, for each case
- [ ] Encrypt/Decrypt password (that can be shown) 🔒
- [ ] Hash password (that can't be shown) 🗝️
- [ ] Create a category 📓
- [ ] Manage existing categories 📝
- [ ] Save into files 💾
- [ ] Load from files 🔄
- [ ] Be able to copy username + password with one click (customizable delay) 🏎
- [ ] Shortcuts for most used
- [ ] Quick search
- [ ] Basic shell UI
- [ ] Settings ⚙

## Done ✔
- [x] Nothing 😢

## Ideas 💡
- Make sure only this computer can access the program (first time launch -> need the password, that will be hashed somewhere to prove the computer is authorized)
- Some passwords are less important, so no password asked to show them
- Some passwords are important, so a password asked everytime to show them (this password can be global or chosen when created)
- The encryption algorithm for "showable passwords" need to be non-crackable without the password chosen (encryption/decryption with the password as key which is never saved)