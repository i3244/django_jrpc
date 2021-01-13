from django.http import JsonResponse
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from jsonrpcserver import method, dispatch

import ipware

@csrf_exempt
def jsonrpc(request):
    ipaddress, _ = ipware.get_client_ip(request)

    if not ipaddress.startswith("192.168.1."):
        return HttpResponse(status=400)

    response = dispatch(
        request=request.body.decode(), context={'ipaddress': ipaddress}
    )
    return JsonResponse(
        response.deserialized(), status=response.http_status, safe=False
    )

@method
def ping():
    return "pong"

# 引数リストにcontextを追加する
@method
def division(context, dividend, divisor):
    # コンテキストからIPアドレスを取り出す
    ipaddress = context['ipaddress']
    # IPアドレスを戻り値に追加する
    return {"quotient": dividend // divisor, "remainder": dividend % divisor, "ipaddress": ipaddress}
