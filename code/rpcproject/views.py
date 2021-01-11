from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from jsonrpcserver import method, dispatch

# ライブラリを追加でインポート
import ipware

@csrf_exempt
def jsonrpc(request):
    # requestオブジェクトからクライアントのIPアドレスを抽出する
    ipaddress, _ = ipware.get_client_ip(request)

    # jsonrpcserver.dispatch関数の引数にコンテキストを追加する
    response = dispatch(request=request.body.decode(), context={'ipaddress': ipaddress})
    return JsonResponse(
        response.deserialized(), status=response.http_status, safe=False
    )

# 引数リストにcontextを追加する
@method
def division(context, dividend, divisor):
    # コンテキストからIPアドレスを取り出す
    ipaddress = context['ipaddress']
    # IPアドレスを戻り値に追加する
    return {"quotient": dividend // divisor, "remainder": dividend % divisor, "ipaddress": ipaddress}
