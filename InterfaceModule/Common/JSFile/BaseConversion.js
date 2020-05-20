    // 补全ipv6
    function ipv6_to_hex(address) {
        var ipv6_to_16 = '';
        var ipv6_1 = [];
        var number_1 = 0;
        var number = 0;
        var flag = true;
        if (address.indexOf("::") > -1) {
            var ipv6 = address.split("::");
            for (var i = 0; i < ipv6.length; i++) {
                if (ipv6[i].indexOf(':') > 0) {
                    var t = ipv6[i].split(':');
                    if (flag) {
                        number_1 = t.length
                    }
                    number = number + t.length
                    for (var j = 0; j < t.length; j++) {
                        if (t[j].length != 4) {
                            var a = "0000";
                            var s = a.substring(0, 4 - t[j].length);
                            var b = s.concat(t[j]);
                            ipv6_1.push(b)
                        } else {
                            ipv6_1.push(t[j]);
                        }
                    }
                    flag = false
                } else {
                    if (ipv6[i].length != 4) {
                        var a = "0000";
                        var s = a.substring(0, 4 - ipv6[i].length);
                        var b = s.concat(ipv6[i]);
                        ipv6_1.push(b)
                    } else {
                        ipv6_1.push(ipv6[i]);
                    }
                    if (flag) {
                        number_1 = number_1 + 1
                    }
                    number = number + 1;
                    flag = false
                }
            }

            var v = "0000";
            var ipv6_3 = '';
            for (var h = 0; h < 8 - number; h++) {
                ipv6_3 = ipv6_3.concat(v)
            }
            for (var y = 0; y < ipv6_1.length; y++) {
                if (y == number_1) {
                    ipv6_to_16 = ipv6_to_16.concat(ipv6_3)
                    ipv6_to_16 = ipv6_to_16.concat(ipv6_1[y])
                } else {
                    ipv6_to_16 = ipv6_to_16.concat(ipv6_1[y])
                }

            }
            return ipv6_to_16
        } else {
            var ipv6 = address.split(":");
            for (var i = 0; i < ipv6.length; i++) {
                if (ipv6[i].length != 4) {
                    var a = "0000";
                    var s = a.substring(0, 4 - ipv6[i].length);
                    var b = s.concat(ipv6[i]);
                    ipv6_to_16 = ipv6_to_16.concat(b);
                } else {
                    ipv6_to_16 = ipv6_to_16.concat(ipv6[i]);
                }
            }
            return ipv6_to_16
        }
    }

    // ipv6转二进制（需先补全）
    function hex_to_bin(str) {
        var hex_array = [{key: 0, val: "0000"}, {key: 1, val: "0001"}, {key: 2, val: "0010"}, {
            key: 3,
            val: "0011"
        }, {key: 4, val: "0100"}, {key: 5, val: "0101"}, {key: 6, val: "0110"}, {key: 7, val: "0111"},
            {key: 8, val: "1000"}, {key: 9, val: "1001"}, {key: 'a', val: "1010"}, {key: 'b', val: "1011"}, {
                key: 'c',
                val: "1100"
            }, {key: 'd', val: "1101"}, {key: 'e', val: "1110"}, {key: 'f', val: "1111"}];

        var value = "";
        for (var i = 0; i < str.length; i++) {
            for (var j = 0; j < hex_array.length; j++) {
                if (str.charAt(i).toLowerCase() == hex_array[j].key) {
                    value = value.concat(hex_array[j].val);
                    break;
                }
            }
        }
        return value;
    }

    // 二进制转16进制
    function bin_to_hex(str) {
        let hex_array = [{key: 0, val: "0000"}, {key: 1, val: "0001"}, {key: 2, val: "0010"}, {
            key: 3,
            val: "0011"
        }, {key: 4, val: "0100"}, {key: 5, val: "0101"}, {key: 6, val: "0110"}, {key: 7, val: "0111"},
            {key: 8, val: "1000"}, {key: 9, val: "1001"}, {key: 'a', val: "1010"}, {key: 'b', val: "1011"}, {
                key: 'c',
                val: "1100"
            }, {key: 'd', val: "1101"}, {key: 'e', val: "1110"}, {key: 'f', val: "1111"}]
        let value = ''
        let list = []
        // console.log(str)
        if (str.length % 4 !== 0) {
            let a = "0000"
            let b = a.substring(0, 4 - str.length % 4)
            str = b.concat(str)
        }
        // console.log(str)
        while (str.length > 4) {
            list.push(str.substring(0, 4))
            str = str.substring(4);
        }
        list.push(str)
        // console.log(list)
        for (let i = 0; i < list.length; i++) {
            for (let j = 0; j < hex_array.length; j++) {
                if (list[i] == hex_array[j].val) {
                    value = value.concat(hex_array[j].key)
                    break
                }
            }
        }
        // console.log(value)
        return value
    }

    // 补全ipv4
    function ipv4_to_hex(address) {
        var ipv4_to_all = '';
        var ipv4 = address.split(".");
        for (var i = 0; i < ipv4.length; i++) {
            if (ipv4[i].length != 3) {
                var a = "000";
                var s = a.substring(0, 3 - ipv4[i].length);
                var b = s.concat(ipv4[i]);
                ipv4_to_all = ipv4_to_all.concat(b);
            } else {
                ipv4_to_all = ipv4_to_all.concat(ipv4[i]);
            }
        }
        return ipv4_to_all
    }

    // ipv4转二进制
    function ipv4_to_bin(ipv4All) {
        var temp = parseInt(ipv4All);
        ipv4ToTwo = temp.toString(2);
        return ipv4ToTwo
    }

    // 二进制转ipv4
    function two_to_ipv4(address) {
        ipv4 = parseInt(address, 2);//转成十进制
        return ipv4;
    }
