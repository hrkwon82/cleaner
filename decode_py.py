# 2019-9-17

import js2py

def decode(service_code_origin,r_value):

    decode_service_code='''
    function get_service_code(service_code, r_value){

        var a,e,n,t,f,d,h,i = "yL/M=zNa0bcPQdReSfTgUhViWjXkYIZmnpo+qArOBs1Ct2D3uE4Fv5G6wHl78xJ9K",
        o = "",
        c = 0;
        for (r_value = r_value.replace(/[^A-Za-z0-9+/=]/g,""); c < r_value.length;) {
            t = i.indexOf(r_value.charAt(c++));
            f = i.indexOf(r_value.charAt(c++));
            d = i.indexOf(r_value.charAt(c++));
            h = i.indexOf(r_value.charAt(c++));
            a = t << 2 | f >> 4;
            e = (15 & f) << 4 | d >> 2;
            n = (3 & d) << 6 | h;
            o += String.fromCharCode(a);
            64 != d && (o += String.fromCharCode(e));
            64 != h && (o += String.fromCharCode(n));
        }
        var tvl = o;
        var fi = parseInt(tvl.substr(0,1));
        fi = fi > 5 ? fi - 5 : fi + 4;
        var _r = tvl.replace(/^./, fi);
        var _rs = _r.split(",");
        var replace = "";
        for (e = 0; e < _rs.length; e++) replace += String.fromCharCode(2 * (_rs[e] - e - 1) / (13 - e - 1));
        return service_code.replace(/(.{10})$/, replace)
    }
    '''

    
    decode_service_code = js2py.eval_js(decode_service_code)

    service_code = decode_service_code(service_code_origin, r_value)

    return service_code