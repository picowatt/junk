Streaming radio by way of Redis.

rtl_fm -M wbfm -f89.7M | sox -traw -r24k -es -b16 -c1 -V1 - -tmp3 - | socat -u - TCP-LISTEN:6789