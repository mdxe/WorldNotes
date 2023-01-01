## World Notes

Simple Flask/Python/SQLite/OpenStreetMap app where you can save a picture and a note for a specific location on a map.


## Usage

1. Start server

```bash
> python app.py
```

2. Navigate to: http://127.0.0.1:5000/

3. Right click to add a map note.

Demo: https://flatbottom.pythonanywhere.com

Screenshot: https://i.imgur.com/9Cp6g64.png

## Todo

- [ ] read GPS data from pic and set coordinates
- [ ] add authentication and private worlds
- [ ] fix lighttpd hosting


- [X] fix file upload
- [X] on click for existing point -> popup edit form
- [X] add coordinates and zoom to url so that a reload doesn't move the view
- [X] change marker to red if no picture available
- [X] allow soft delete
- [X] block overwriting of data or files
- [X] display file uploaded (text or image)
- [X] change mouse pointer when over a marker
- [X] add ability to change images
- [X] Combine lat/long in form to save space
- [X] put all form button on same line to save space

## Credits

Thanks to Flask-with-DB: https://github.com/Ruhil-DS/Flask-with-DB, which this project is based on.



