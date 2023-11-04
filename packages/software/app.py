# Flask-APIを構築するための基本機能
from flask import Flask

# CORSライブラリ
from flask_cors import CORS

# ルーター: ルーティング設定
import router

def create_app():

    # Flask-Appを立ち上げる & templateのDirを指定する
    app = Flask(__name__)

    # Router を Flask-App に登録する && URL_末尾に /api を追加する
    app.register_blueprint(router.router, url_prefix='/api')

    # CORS許可でアプリを包む => APIへのCORS許可設定
    CORS(app)
    # resources={r"/api/*": {"origins": "http://localhost:8001"}}
    return app

app = create_app()
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8081, threaded=True, use_reloader=False)
