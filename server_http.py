from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from shap_e.mylib.modelCreate import model_create
import cgi
import tempfile
import os

class Handler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server, xm, model, diffusion):
        self.xm = xm
        self.model = model
        self.diffusion = diffusion
        super().__init__(request, client_address, server)

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        print(f"file get")
        # Assuming the POST data includes a file and its name
        fileitem = form['file']
        filename = form['filename'].value
        client_id = form['client_id'].value

        client_data = {}

        if fileitem.file:
            file_data = fileitem.file.read()
            client_data[client_id] = file_data
            _, extension = os.path.splitext(filename)  # Extract extension from filename
            img_temp = tempfile.NamedTemporaryFile(suffix=extension, delete=False, mode="w+b")
            with open(img_temp.name, 'wb') as f:
                f.write(file_data)
            img_temp.close()  # Close the file before passing its path to model_create
            # crete model via shap_e
            model_create(self.xm, self.model, self.diffusion, img_temp.name)

            # # It's an uploaded file; save it with its original extension
            # with open(f"./{filename}", "wb") as fout:
            #     fout.write(file_data)

            
            # Save client id and image data to the dictionary
            
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'File received and saved.')

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, xm, model, diffusion):
        self.RequestHandlerClass = lambda *args, **kwargs: RequestHandlerClass(*args, **kwargs, xm=xm, model=model, diffusion=diffusion)
        super().__init__(server_address, self.RequestHandlerClass)
    # """Handle requests in a separate thread."""

# if __name__ == "__main__":
#     server = ThreadedHTTPServer(('0.0.0.0', 8086), Handler)
#     server.serve_forever()