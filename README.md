## World Notes

Simple Flask/Python/SQLite/OpenStreetMap app where you can save a picture and a note for a specific location on a map.


## Usage

1. Start server

```bash
> python app.py
```

2. Navigate to: http://127.0.0.1:5001/

3. Right click to add a map note.

Demo: https://flatbottom.pythonanywhere.com

Screenshot: https://i.imgur.com/9Cp6g64.png

## Todo

- [ ] read GPS data from pic and set coordinates according to that instead (optional)
- [ ] add authentication and private worlds
- [ ] fix lighttpd hosting
- [ ] warn or prevent when overwriting file
- [X] Combine lat/long in form to save space
- [X] put all form button on same line to save space


## Credits

Thanks to Flask-with-DB: https://github.com/Ruhil-DS/Flask-with-DB, which this project is based on.



