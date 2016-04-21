import inspect
import sys
import pprint

VARIABLES = {
"S1" : "3939252352554c5f51592621294d5c5229382f5d454b485d4554413132275458482d3157415046495c5b2a435a46543527364d5059394847382a2b4b555746404a38202d4c525652455c2a",
"S2" : "4d514c503134405f305f4e44292c41534a57414f2c2c2d4054544d5f552741424c5931345f415d2c2e4d4454405e504142522e31424a434c5f2a2b415a412f585a55452d2e20394941562a",
"S3" : "56574023455d4449305b4745295b5b5a45385f59435a44574526453132445c5a454843404d585a2c4146464e3246544146554531445c49574a435f573a",
"S4" : "505725575951292c53594f515d435544484847522c2c4e5f4155575441274c45582d465d444c2e404b495859324f4f4227424131545644444d594e2e554a4b2c4757204947465f4c53572a",
"S5" : "4d5625565f504c5e435f474f4d2c565f5a5b5d4e58492d4352494650504e59435954315d5b2047415e4758435349543553592e44595d4f504b5e4a4050244c5e4a48544249525849484b2a",
"S6" : "5c57424f5847412c5c4e52554c5e41364f4a4a5a594943505926455d5e4842592d545e412854412c4c5a4f565927565c40534054455c2a43564e2b4d55415c4d413843445e485c4b533c",
"S7" : "5a4b5c53455b4e5e515b4e5829454136594a4a584942593349482442575150584c413150414648495c4d44433253594542452e5e51394b524846424d555046435d4b20434157585d414b5722",
"S8" : "505f255a5e41294a5f5e484529585a532957414e2c58445e45265450562b355e45485f34514f5b2c46495c523241495b4e45465453395e4a51592b2e574b5a5e405d57425c4b37",
"S9" : "5c6f607168346a607f7e6221616d613668387c62607a6861206a6d7f7b697224"
}

class MyOperations():
    def help(self):
        """See all the available operations, params and helper and all"""
        result = "=> Available Commands:\n"
        for o in inspect.getmembers(self, inspect.ismethod):
            if "_" not in o:
                result += "\t"
                result += o[0]
                result += " - "
                result += "params:" + str(inspect.getargspec(o[1])[0][1:])
                result += " - "
                result += str(inspect.getdoc(o[1]))
                result += "\n"
        return result
        
    def var(self):
        """See all the available variables and their current value"""
        result = "=> Current Variables and values:\n"
        for v in sorted(VARIABLES.keys()):
            result += "\t" + v + " = " + VARIABLES[v] + "\n"
        return result

    def store(self, p, v):
        """Stored a value on variables area"""
        VARIABLES[p] = v
        return "VARIABLES[{0}] = {1}".format(p, v)
        
    def exit(self):
        """Closes the program"""
        return "exit"
        
    def to_hex(self,s):
        """Convert some string to hexadecimal"""
        return s.encode("hex")
        
    def to_hex_store(self,p,s):
        """Convert some string to hexadecimal and store"""
        v = self.to_hex(s)
        return self.store(p, v)

    def from_hex(self,s):
        """Convert some string from hexadecimal"""
        return s.decode("hex")
        
    def from_hex_store(self,p,s):
        """Convert some string from hexadecimal and store"""
        v = self.from_hex(s)
        return self.store(p, v)
        
    def get_readable_only(self,s):
        """Convert some string from hexadecimal to a readable one - or a '.'"""
        result = ""
        for i in range(0, len(s), 2):
            v = int(s[i:i+2],16)
            if v == 32 or (v >= 65 and v <= 90) or (v >= 97 and v <= 122):
                result += chr(v)
            elif v == 0:
                result += "0"
            else:
                result += "."
        return result

    def xor_strings(self, xs, ys):
        """Apply a xor operation on two strings"""
        return "".join([("%0.2X" % (ord(x) ^ ord(y))).lower() for x, y in zip(xs, ys)])
        
    def xor_strings_store(self, p, xs, ys):
        """Apply a xor operation on two strings and store it"""
        v = self.xor_strings(xs, ys)
        return self.store(p, v)
        
    def xor_strings_store_output(self, p, xs, ys):
        """Apply a xor operation on two strings and store it"""
        v = self.xor_strings(xs, ys)
        return self.store(p, self.from_hex(v))
        
    def xor_strings_store_from_hex(self, p, xs, ys):
        """Apply a xor operation on two hexadecimal strings and store it as resulted"""
        v = self.xor_strings(self.from_hex(xs), self.from_hex(ys))
        return self.store(p, v)
        
    def xor_strings_store_from_hex_output(self, p, xs, ys):
        """Apply a xor operation on two hexadecimal strings (xs and ys) after conversion and store it as hexadecimal (on p)"""
        v = self.xor_strings(self.from_hex(xs), self.from_hex(ys))
        return self.store(p, self.from_hex(v))
        
    def store_space_hex(self, p, var):
        """Create a string with hexadecimal spaces (0x20) the len of 'var' and store it on 'p'"""
        return self.store_char_hex(p, var, " ")
        
    def store_space(self, p, var):
        """Create a string spaces (' ') with the len of 'var' and store it on 'p'"""
        return self.store_char(p, var, " ")
        
    def store_char_hex(self, p, var, char):
        """Create a string with hexadecimal chars the len of 'var' and store it on 'p'"""
        return self.store_char(p, var, self.to_hex(char))
        
    def store_char(self, p, var, char):
        """Create a string of chars with the len of 'var' and store it on 'p'"""
        v = "".join([char for i in range(0, len(var))])
        return self.store(p, v)
        
    def store_word_hex(self, p, var, word):
        """Create a string with hexadecimal words the len of 'var' and store it on 'p'"""
        return self.store_word(p, var, self.to_hex(word))
        
    def store_word(self, p, var, word):
        """Create a string of words with the len of 'var' and store it on 'p'"""
        spaces_to_fill_var = int(len(var) - len(word))
        v = word + (" "*spaces_to_fill_var)
        return self.store(p, v)

def unpack_expected_params(params, expected_number):
    if len(params) != expected_number:
        return ("Bad params: {0} expected, {1} received".format(expected_number, len(params)), range(0, expected_number))
    return ("", params)
    
def decode_params(params):
    real_params = []
    for p in params:
        p = p.strip(" ")
        if p in VARIABLES:
            real_params.append(VARIABLES[p])
        elif "*" in p and p.replace("*","") in VARIABLES:
            real_params.append(p.replace("*",""))
        elif "'" in p:
            real_params.append(p.replace("'",""))
        else:
            real_params.append(p)
    return real_params
    
def separate_operation_params(operation):
    op = operation[:operation.find("(")] if operation.find("(") >= 0 else operation
    params = operation[operation.find("(")+1:operation.find(")")].split(",") if operation.find("(") >= 0 else []
    return (op, decode_params(params))

def function_by_name(op):
    return [f[1] for f in inspect.getmembers(globals()['MyOperations'](), inspect.ismethod) if f[0] == op][0]

def call_by_name(op, params):
    return getattr(globals()['MyOperations'](), op)(*tuple(params))
    
def parse_operation(operation):
    op,params = separate_operation_params(operation)
    if op not in dir(MyOperations):
        return "Bad operation: " + op
    expected_params_len = len(inspect.getargspec(function_by_name(op))[0]) - 1 #remove self
    params_err, s = unpack_expected_params(params, expected_params_len)
    if len(params_err) > 0:
        return params_err
    result = call_by_name(op, params)
    return result

def saved_operations_from_file(f):
    saved_operations = []
    with open(f, 'r') as f:
        saved_operations = [l.replace("\r","").replace("\n","") for l in f.readlines()]
    return saved_operations
        
def saved_operations_to_file(f,saved_operations):
    with open(f, 'w') as f:
        for s in saved_operations:
            f.write(s + "\n")

def restore_previous_state():
    saved_operations = saved_operations_from_file("operations.txt")
    for s in saved_operations:
        try:
            parse_operation(s)
        except Exception as e:
            print s,"Exception:",e
    print parse_operation("help")
    print parse_operation("var")
    return saved_operations
    
def save_state(saved_operations):
    print saved_operations  
    saved_operations_to_file("operations.txt", saved_operations)
    
def main_loop(saved_operations):
    exit = False
    while not exit:
        try:
            operation = raw_input('--> ')
            result = parse_operation(operation)
            if result == "exit":
                exit = True
            else:
                print result
                if not "Bad Operation" in result:
                    saved_operations.append(operation)
        except Exception as e:
            print e
            exit = True
    return saved_operations
    
def apply_crib(op, result, x_name, xplain, i, crib_name, crib_value, ignore_readable = False, ignore_attrib = False):
    slice = xplain[i:i+len(crib_value)]
    x_xor_c = op.xor_strings(slice, crib_value)
    readable = op.get_readable_only(x_xor_c)
    result_position = " xor ".join([x_name,crib_name])
    if len(readable) > 5 and (ignore_readable or readable.find(".") < 0):
        if not ignore_attrib:
            result[result_position] = readable
        return True
    else:
        return False

def crib_dragging():
    saved_operations = []
    pair_of_keys = [(x,y) for x in sorted(VARIABLES.keys()) for y in sorted(VARIABLES.keys()) if x != y and y > x]
    cribs = {   "Ans": "an ", 
                "As": "as ", 
                "Ifs": "if ", 
                "Ofs": "of ", 
                "Ons": "on ", 
                "Mys": "my ", 
                "Mes": "me ", 
                "Was": "was ", 
                "Weres": "were ", 
                "Whos": "who ", 
                "What": "what ",
                "Hands": "hand ",                 
                "Ares": "are ", 
                "Yous": "you ",
                "Ends": "end ",
                "Is" : "is ",
                "Nos" : "no ",
                "Dos" : "do ",
                "Bys" : "by ",
                "Gets" : "get ",
                "Gots" : "got ",
                "Ins" : "in ",
                "Ats" : "at ",
                "Hes" : "he ",
                "Us" : "us ",
                "Wes" : "we ",
                "Gos" : "go ",
                "God" : "god ",
                "Tcps" : "tcp",
                "Age" : "age ",
                "Aid" : "aid ",
                "Lies" : "lie ",
                "Buts" : "but ",
                "Lads" : "lad ",
                "Ors" : "or", 
                "Agos" : "ago", 
                "Fors" : "for", 
                "Exits" : "exit", 
                "Runs" : "run", 
                "Ones" : "one", 
                "Mads" : "mad", 
                "Uses" : "use", 
                "Days" : "day", 
                "Typo" : "typo",
                "Pads": "pad", 
                "Hole":"hole",
                "Fakes":"fake",
                "Wars":"war",
                "Attacks" : "attack ",
                "Classes" : "classes ",
                "Wants" : "want ",
                "He created" : "he created ",
                "THATs":"that", 
                "Easy" : "easy ",
                "Easilys" : "at can be easily broken",
                "Easilys Brokens" : " easily broken",
                "THEs":"the",
                "Trues":"true",
                "Homes" : "home", 
                "english" : "english",
                "Types of ":"types of a",
                "The Timess":"the times",
                "THIS ISs":"this is", 
                "THIS IS THEs":"this is the", 
                "Wills":"will", 
                "Unders":"under", 
                "Everys":"every", 
                "Silver":"silver", 
                "Cryptos":"crypto", 
                "Cryptography":"cryptography", 
                "Cryptography Classes":" cryptography classes ", 
                "Ands" : "and", 
                "Codes" : "code", 
                "Variables" : "variable", 
                "Prints": "print", 
                "Times":"time",
                "Usings":"using ",
                "Using ons":"using on ",
                "If you":"if you",
                "In The":" in the ",
                "Strings" : " string ",
                "Vigeneres":" vigenere ",
                "Vigeneres and caesar":" vigenere and caesar ",
                "World War":"world war",
                "if you found" : "if you found th",
                "Nowaday" : "nowaday",
                "provide a" : "provide a",
                "Provides" : "provide ",
                "Present in" : " present in security",
                "Finished" : "finished ",
                "Frequency" : "frequency ",
                "if you found" : " if you found ",
                "frequency anali" : "frequency anali",
                "Letters Frequency" : " letters frequency",
                "in the cripto" : "in the cripto",
                "Confuse" : " confuse ",
                "To diffuse" : " to diffuse ",
                "Every cloud" : " every cloud ",
                "to understand" : "to understand",
                "english letters" : "english letters",
                "One Strings" : "one string",
                "Second Strings" : "second string",
                "One Time" : "one time",
                "One Time Pads" : "one time pad",
                "IS_THE" : " is the ",
                "THIS_IS_THE" : "this is the ",
                "Caesars" : "caesar ",
                "Caesars Ans" : "caesar an",
                "Caesar and Vigenere" : "caesar and vigenere",
                "Of applications": " of applications"}
    op = MyOperations()
    result = {}
    analisis = {}
    cribs_analisis = {}
    
    for x,y in pair_of_keys:
        result = {}
        print "SS","".join([str(i % 10) for i in range(1,len(VARIABLES[x])/2)])
        print x,op.get_readable_only(VARIABLES[x])
        print y,op.get_readable_only(VARIABLES[y])
        if x not in analisis: analisis[x] = {}
        if y not in analisis: analisis[y] = {}
        
        xplain = op.from_hex(VARIABLES[x])
        yplain = op.from_hex(VARIABLES[y])
        x_xor_y = op.xor_strings(xplain, yplain)
        plain_x_xor_y = op.get_readable_only(x_xor_y)
        hex_x_xor_y = op.from_hex(x_xor_y)
        print x,y,plain_x_xor_y
        for c in cribs.keys():
            limit = len(hex_x_xor_y) - len(cribs[c])
            if cribs[c] not in cribs_analisis: 
                cribs_analisis[cribs[c]] = {}
                cribs_analisis[cribs[c]]["count"] = {}
                cribs_analisis[cribs[c]]["indexes"] = {}
            for i in range(0,limit):
                crib_name = c + "_" + ("%0.2d" % (i))
                worked = apply_crib(op, result, " xor ".join([x,y]),hex_x_xor_y, i, crib_name, cribs[c], False, False)
                if worked:
                    if cribs[c] not in analisis[x]: analisis[x][cribs[c]] = 0
                    if x not in cribs_analisis[cribs[c]]["count"]: cribs_analisis[cribs[c]]["count"][x] = 0
                    if x not in cribs_analisis[cribs[c]]["indexes"]: cribs_analisis[cribs[c]]["indexes"][x] = []
                    if cribs[c] not in analisis[y]: analisis[y][cribs[c]] = 0
                    if y not in cribs_analisis[cribs[c]]["count"]: cribs_analisis[cribs[c]]["count"][y] = 0
                    if y not in cribs_analisis[cribs[c]]["indexes"]: cribs_analisis[cribs[c]]["indexes"][y] = []
                    analisis[x][cribs[c]] += 1
                    cribs_analisis[cribs[c]]["count"][x] += 1
                    cribs_analisis[cribs[c]]["indexes"][x].append(crib_name)
                    analisis[y][cribs[c]] += 1
                    cribs_analisis[cribs[c]]["count"][y] += 1
                    cribs_analisis[cribs[c]]["indexes"][y].append(crib_name)
                    apply_crib(op, result, x, xplain, i, crib_name, cribs[c], False, False)
                    apply_crib(op, result, y, yplain, i, crib_name, cribs[c], False, False)
        pp = pprint.PrettyPrinter(indent=2)
        print pp.pprint(result)
        
    print "Analisis:"
    for x in analisis.keys():
        print x,analisis[x]
    print pp.pprint(analisis)
    print pp.pprint(cribs_analisis)

def avelino_brute_force():
    op = MyOperations()
    possible_bytes = [i for i in range(0,255)]
    where_to_begin = 73 #0 
    max_index = max([len(VARIABLES[x]) for x in VARIABLES.keys()])
    result = {i:[] for i in range(where_to_begin, max_index)}
    for index in range(where_to_begin, max_index):
        for pb in possible_bytes:
            is_readable = True
            readables = []
            #for x in ["S1","S2","S3","S4","S5","S6","S7","S8"]:
            for x in ["S1","S2","S4","S5"]:
                xplain = op.from_hex(VARIABLES[x])
                if is_readable and index < len(xplain):
                    xored = ("%0.2X" % (ord(xplain[index]) ^ pb))
                    readable = op.get_readable_only(xored)
                    readables.append(x + ":" + readable)
                    if readable in ["."]:
                        #print "{0} failed on {1} of {2}".format("%0.2X" % pb, index, x)
                        is_readable = False
            if is_readable:
                result[index].append("%0.2X" % pb + " - " + str(readables))
    
    for r in sorted(result.keys()):
        print r, result[r]

def decrypt_all(key, ignore_positions):
    op = MyOperations()
    for x in ["S1","S2","S3","S4","S5","S6","S7","S8", "S9"]:
        key_hex = op.from_hex(key)
        var_hex = op.from_hex(VARIABLES[x])
        
        #pad key if needed
        if len(key_hex) < len(var_hex):
            key_hex += " "*(len(var_hex) - len(key_hex))
        
        length_to_use = min(len(key_hex), len(var_hex))
                
        for i in ignore_positions:
            if i < length_to_use:
                key_hex = key_hex[:i] + var_hex[i] + key_hex[i+1:]
        
        plain = op.xor_strings(var_hex, key_hex[:length_to_use])
        print x,op.from_hex(plain)
        
if __name__ == "__main__":
    if "-c" in sys.argv:
        crib_dragging()
    elif "-a" in sys.argv:
        avelino_brute_force()
    elif "-k" in sys.argv:
        key = "191905031114090C100B0601090C121609180F0B0C0C0D13000604111220150A0D0D111408000E0C0E080A171207001507160E1117190A02180A0B0E00040F0C1318000D0E0000190012"
        decrypt_all(key, [29,60,70])
    else:
        saved_operations = restore_previous_state()    
        saved_operations = main_loop(saved_operations)
        save_state(saved_operations)