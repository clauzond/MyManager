# MyManager 🛡

## Why ❓
➡ manage all my accounts (websites, games, ...)  
➡ quickly copy/paste account  
➡ safely save passwords  

## How to launch 🚀
Simply run `main.py`

## Todo ⏳
- [ ] Add tags 🏷
- [ ] Quick search 🔎
- [ ] Better shell UI 🖼

## Done ✔
- [x] Choose every algorithm needed, for each case
- [x] Encrypt/Decrypt password (that can be shown) 🔒
- [x] Hash password (that can't be shown) 🗝️
- [x] Create/modify an account 📕
- [x] Create/modify a category 📓
- [x] Create/modify favorites category ♥
- [x] Nice menu, being able to go back...
- [x] Be able to copy username + password with one click (customizable delay) 🏎
- [x] Shortcuts for most used 🛎
- [x] Settings ⚙

## Ideas 💡
- Make sure only this computer can access the program (first time launch -> need the password, that will be hashed somewhere to prove the computer is authorized)
- Some passwords are less important, so no password asked to show them
- Some passwords are important, so a password asked everytime to show them (this password can be global or chosen when created)
- The encryption algorithm for "showable passwords" need to be non-crackable without the password chosen (encryption/decryption with the password as key which is never saved)