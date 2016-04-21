from friedman_find_key_len import *
from vigenere import *

import unittest

class TestBreakHelperMethods(unittest.TestCase):
    def setUp(self):
        print "="*10 + self._testMethodName

    def test_break_message_in_1_column(self):
        self.assertEqual(break_message_in_columns("123", 1), 
                        {
                        0:['1','2','3']
                        })
        self.assertEqual("123",
                          assemble_message_from_columns(["123"]))
    def test_break_message_in_2_columns(self):
        self.assertEqual(break_message_in_columns("123456", 2), 
                        {
                        0:['1','3','5'], 
                        1:['2','4','6']
                        })
        self.assertEqual("123456",
                          assemble_message_from_columns(["135","246"]))
    def test_break_message_in_2_columns_even(self):
        self.assertEqual(break_message_in_columns("1234567", 2), 
                        {
                        0:['1','3','5','7'], 
                        1:['2','4','6']
                        })
        self.assertEqual("1234567",
                          assemble_message_from_columns(["1357","246"]))
    def test_break_message_in_3_columns_even(self):
        self.assertEqual(break_message_in_columns("1234567", 3), 
                        {
                        0:['1','4','7'], 
                        1:['2','5'],
                        2:['3','6']
                        })
        self.assertEqual("1234567",
                          assemble_message_from_columns(["147","25","36"]))
    def test_count_occurences_all_1(self):
        self.assertEqual(count_occurences(['1','2','3','4']),
                         {
                         '1':1,
                         '2':1,
                         '3':1,
                         '4':1
                         })
    def test_count_occurences_alphabet(self):
        self.assertEqual(count_occurences(['a','c','c','b']),
                         {
                         'a':1,
                         'b':1,
                         'c':2
                         })
    def test_count_occurences_string(self):
        self.assertEqual(count_occurences("afganeuanebcte"),
                         {
                         'a':3,
                         'b':1,
                         'c':1,
                         'e':3,
                         'f':1,
                         'g':1,
                         'n':2,
                         'u':1,
                         't':1
                         })
    def test_coincidence_index_all_same_and_1_len(self):
        self.assertEqual(count_occurences("abc"),
                         {
                         'a':1,
                         'b':1,
                         'c':1
                         })
        self.assertEqual(0, sum_of_counts({
                         'a':1,
                         'b':1,
                         'c':1
                         }))
        self.assertEqual(0, calculate_coincidence_index("abc",['a']))
        self.assertEqual(0, calculate_coincidence_index("abc", ['b']))
        self.assertEqual(0, calculate_coincidence_index("abc", ['c']))
    def test_coincidence_index_all_same_and_2_len(self):
        input = "abcabc"
        expected_columns = {
                        0:['a','a'], 
                        1:['b','b'],
                        2:['c','c']
                        }
        self.assertEqual(count_occurences(expected_columns[0]), {'a':2})
        self.assertEqual(2, sum_of_counts({'a':2}))
        self.assertEqual(1.0, 
                         calculate_coincidence_index("abc", expected_columns[0], True))
        
        self.assertEqual(count_occurences(expected_columns[1]), {'b':2})
        self.assertEqual(2, sum_of_counts({'b':2}))
        self.assertEqual(1.0, 
                        calculate_coincidence_index("abc", expected_columns[1]))
        
        self.assertEqual(count_occurences(expected_columns[2]), {'c':2})
        self.assertEqual(2, sum_of_counts({'c':2}))
        self.assertEqual(1.0, 
                        calculate_coincidence_index("abc", expected_columns[2]))
    def test_calculate_column_wise_coincidence_index(self):
        input = "abcabcabc"
        expected_columns = {
                        0:['a','a','a'], 
                        1:['b','b','b'],
                        2:['c','c','c']
                        }
        self.assertEqual(expected_columns, break_message_in_columns(input, 3))
        self.assertEqual(count_occurences(expected_columns[0]), {'a':3})
        self.assertEqual(count_occurences(expected_columns[1]), {'b':3})
        self.assertEqual(count_occurences(expected_columns[2]), {'c':3})
        self.assertEqual(6, sum_of_counts({'a':3}))
        self.assertEqual(6, sum_of_counts({'b':3}))
        self.assertEqual(6, sum_of_counts({'c':3}))
        self.assertEqual(1.0, 
                        calculate_coincidence_index("abc", expected_columns[0], True))
        self.assertEqual(1.0, 
                        calculate_coincidence_index("abc", expected_columns[1]))
        self.assertEqual(1.0, 
                        calculate_coincidence_index("abc", expected_columns[2]))
        self.assertEqual( 1.0, 
                         calculate_column_wise_coincidence_index("abcabcabc", 3))

    def _clear_chars(self, message, char):
        return message.replace(char, "")
        
    def test_best_key_len_with_1_len(self):
        key = 'Y'
        message = self._clear_chars("DO OR DO NOT THERE IS NO TRY", " ")
        cyphertext = encryptMessage(key, message)
        print friedman(cyphertext)
        self.assertEqual(1, find_best_key_len(cyphertext))
        
    def test_decrypt_monoalphabetic(self):
        key = 'C'
        original = "DEFEND THE EAST WALL OF THE CASTLE"
        message = self._clear_chars(original, " ")
        cyphertext = encryptMessage(key, message)
        print friedman(cyphertext)
        self.assertEqual(message, move_letters_based_on_frequency_analysis(cyphertext))
        
    def test_best_key_len_with_2_len(self):
        key = 'YO'
        message = self._clear_chars("DO OR DO NOT THERE IS NO TRY BECAUSE I AM SAYING THAT THERE IS NO TRY", " ")
        cyphertext = encryptMessage(key, message)
        print friedman(cyphertext)
        self.assertEqual(2, find_best_key_len(cyphertext, True))
        
    def test_best_key_len_wikipedia(self):
        cyphertext = self._clear_chars("""QPWKA LVRXC QZIKG RBPFA EOMFL  JMSDZ VDHXC XJYEB IMTRQ WNMEA IZRVK CVKVL XNEIC FZPZC ZZHKM  LVZVZ IZRRQ WDKEC HOSNY XXLSP MYKVQ XJTDC IOMEE XDQVS RXLRL  KZHOV"""," ")
        print friedman(cyphertext)
        self.assertEqual(5, find_best_key_len(cyphertext))
        
    def test_best_key_len_stinson(self):
        #from Cryptography Theory And Practice by Douglas Stinson
        cyphertext = """CHREEVOAHMAERATBIAXXWTNXBEEOPHBSBQMQEQERBWRVXUOAKXAOSXXWEAHBWGJMMQMNKGRFVGXWTRZXWIAK"""
        print friedman(cyphertext)
        self.assertEqual(5, find_best_key_len(cyphertext, True))
        
    def test_mooodle_class(self):
        cyphertext = """CPIMVTCMNGIHEYCGREMHWLTMVTCEIIQWIVWHMUMHWPTAWGOPTFIZFTGITLEZPCGXFSPSBUCHHBQWHALHDSAOSXYCEISPDTBXOETZWTSMCGJOYOISEGGPDWXZALSTDDWIMWRLLTBSAHRGXNAEDWTLHGDAHRHWPFKOVXEGHDQTASRCIMWPDHTGVTVXBQTRMVIZAPCGWDYOBZULTXNTBCCDEVCCOOGZNTNBAEZRMOCNEMCISEMOAPOYHGZYTBSEHXZTREGRDQAKHWFRTBSTSLOXOALOULCMHDSAOSXYSIWGPDLCBPOYHWPETFAJNTJXRAMCGDOYHWPSBLIPEGHWNEGHJCYMVXDMRHWTCTZILLXCUHHBQWEHXGJMJXQIHALOWTSMCGJOYHWPWTFHZFMVTLTASCTAGGPRABBHETASXDLTBSZFTHALNMWHTSLIEAOLSSEOUSUZUGRTOUICCLNNBUTNBGWPDICTXOYGDWOGHDHHBQWTTPCJWDAOKPSMCDOIGHWPSTATCEEOITOGOHEHXKGTTBBVDOYHWPLHUDRRTDWPRLHDEHXDDPMLCUSOFSGTTPCJWDAOKPTHZSZFTGICUZUAPFHFATBXFIJCIHXXIGHTYDXRIZRXDGPSXBIEHXQDYFEWREOYDTCSBOPYDASAWALKTXARXJOGXTGZMMVTYOUZTNOFATYCXATYTHTISEMWBLENGUCOFHWPFKOVXEGHDQTASRCIMWPDIMGTWFTBSQRHAISEMVXCDUCDVOYHWPLTKHTNPVPEMTBCPRIZPEOPCJWDAOKPTKSPEEWHWTSAWVSAKUJXEGHLPCTBDYLRUJPSLKWJTASVCETHSPSBUCHALOQLNWCCPDISGSAIGQPCTIHPPEOIZBXQPXELSCDIUZTZFLCBPIGQDYGKIXEYBBPQIVHXEIHIHSILHDCYHFQPCTIHPHXVPOLHGISILWCEEKSHEIGWIZRUSRLULSPOVTBRTNZMTLRLTDCBTRTEHXQDXPESITOGCUTTTBSHEFONALXOHPONFHPLOSHHIMVISEYOCNYMVPEHTRISILWBLGBBPCYGOGCAMWKPEOSGMEXBUTNBGWPDPSHSONZSSAOSUZUGREWAMCWTMLSAQSRAELTAWHTNZKXEHMVTDTKIVRLXTDCHXZAPNBQXYDXDTYDXBRPCIZPHSLWCRIGUPSYFBDQTKWJXPACKPRFOGLTACCLNWGPWAFWHAEKVPASFOZTNZHWPRXTAPCMWDYOYVTCOWCIFSPVTCEASRZNMSBALTHTDTASVCOPHWZFMVTLTASCTAGSBAIKSWZWUFPGETHWTNZWHQRXSSZMHTHAEXQWHHBQWSALAPOEMVTLTASCTAGGHZFTFTICXSSPVXFNZTASGDTTHTZFASAWALWCRRXOIYELGDCMHFTARHPPMLROIERBPJEIGUISEOWREOKMIZTASPYCBSCEGHCSZRWSGZFTHWPNLOCOTHHWPFTJDCOYOEZLECPYDTHWPNXQETNMFDOTHQGTTBOHLGTWCALTHDXARPTCEZOGOEWOHEHXQPATTWCLRAQWPGHNDCLXOSPRHTPROHRAJBTBSZFYCAWOPSGDFHFXYTASGPPNPATCBGIZBXTDFNWHWPOKWVTNTZDQCBQTCOLRTCEIIQWIVODQSMOJRULHXYELQXEYHTVZDHTISENHDAITCUDIKHWZMTGBZRXOCOOYHWPNNATCONGDEHXFXXAZWCLRRGILTXGLSIVVPCEYFPXEWIEZNMVTDAFSBZDXZISEXLIPNMHDHHBQWLRBGIZTESDCTASPCILHDEEEWPYSVVDZLPSGPIGRTMTXRIZHBAXYTASEZLBHXNSAOHMEXBATTMZTCEVCVYILSSLNWHWPRXQDRNBHXZNBGISEFCGPNXQTDSTFNMEVOJDEBHXDNHHBLDXPNLRBGIZTESWTMLSAQTASIHOIVXWOLCESEKGWLDFCGPIGQDXMHBISAGHWPYPSGPCHBHNIHIHZFTBSARHPPMLRGDXEXZTXEGHHZFIZPEOKSBLIGGITLEICOEMSREEWWCLRBGIZTESXYEGUATSADWTLHGDAHRHDZMTBNLFYWCTTBSHXARPTERTQTONHHDYLRWCEHXKDCKLCUEHXQPXBKWSREIZPEOGWHESUIITNZFTLTHFXRIGOAHRBHTCSEWZPBXFZPLXMDCCHZTCIWUTEOIZPEOTBSSILWSPALHWLTMVTCEBGPERNHWSIZVTCTAOCPXISGTEGQTZFPVXNHMVTXIGRQPAKGLTTGSHDTHVTCSXZUTSTQDYVBQITOGKWTCAWCZUKCLYGXBTCAMWDYHTGQPEGSCEHNGXLSMWRLLEMPDSXFIPDTBSTSISGSAIGVLIGWCRGKCJYDHTISEZFTPKTIISOKGLSOTHISEKSCLILGPYCXPGZUZVILNXKATFXWCEOMVTHOKZSALTHDSALVPOTASVCETHTDTBBUWUXBRPTASGPPNPATCHTEWAMCXDAEGDEHXTXCSMHGPAMWHPUICCPDNQPEIHBDQWAWRSTASLCIMWCRSHTBTLMCCLNWZDNKXFDFSLSPFJXOCAANZPYDZCTEHXOGPTASAPGBHXXAMSSPSVSCOAGHHWIDSSLNMSDCBNBNLNASWLSTFTGEEOITOGCULNHHWPREWUPLBYTMAVCCSEBGECOYCJYDEMXXPKSHDEWKXEHMVTFNBHNZFDBDHLXRVPIGHWPETFAJCAIGNHASTIEKQXDEWOGPAEWCQLNSCNEHBISEHZDRYTBSLTMVTCEOWKLLHTATTXFPEUKSDYPHZXEIVGTGEGHWPFKOVXEGHHZFAWHHOKRHHHXBGPPXOIPDTHHPCHBSSAGRHJMIVPGEBBPWLTUTDRTJXDHXRISEASPCTLCUXEGKWZHTJTDEXBGPFESREEWWCEHXAISEBFDHNAWVSEKBPEUKSWPILHWPFTHWPRHTXOETZXDMBBESIECHZPAMXYPHZXEIVGXYLBHTCAMIGPAGRBLNRCUEHXZPEELHRZNVSEEIHBHZFFCSPRGHWTNDSGDAGRHEAMSHXEGGJNHTGISENBXEYHTZYOPZTOGXHWPRXWVYOYZPHAGRISEXEJLLBHNZFMVTDEQSHSAOSQPEGOCEIVWELTXRXYAWFTLMUMWTMMVTLRZIBPNMCUEHXFTAUUZXNILHWPSXOGNHTTIPRCIHEIVSISEGOIFRXCUHHBQWTSYWGDTAWCEEWOIMYVSESAEIHEHXXJDTTBSMLTATWELGDWDFOCEHXBSTSVIHDEWCCEHXPPDILCUARHJTCBBOAXOKOATTRPNDOVFPEELOCOPHZTXAKQWFSMVTYCTFXNAMIGPDUMISRTGNXAVVJDAGRELRMWPWLRSMALTWCPDUMHZCKOIPSKSSFCXRIZAGOQDTKOREIHBQJGEOJNOGOCOAWSXXAGHJDAGRWLVBBVMEVCBPIGJXDIUZTTNMVTTNWWKTDNOACETDEPAKGPELXBVEHBBISEBRTLLLHPEEPVXNHBGRZNLHGFCMSSMYLCRCAMSHEHXTXCSMQPCEHTISEKIAPRLWHEOUSTOUVOITOGCUHHBQWLNHIIWIGSXDDKOLYAYHTCTASDWDASAWEGWRXOWSAARHJXOIGUDYLRTDCAGWBARHJTORXZXRIHBPYDFCGLLBHNLNWADCELWBALBQXEYBBBFSBQPYDZMBYALHXNAFOCWIXFHERTWCZFICTERROCOGKSPEEKVPCMHBNZFMVTTNWWKTDNOALNWHWPSMOIPWXOGPTAIHWEWCCEOMVTNOGQTATBCCZFTVXRHXFHEAMSXYWAWRSNHAPYCTZADAGMISIGUWTSHKCLNWWCHHBQWEHXFTTSGSXEHXFBLRKMXYGGCGRIOWCRIGAPCRBOVPAGRZTNZGPCEIVXWOLCESEKGPYDIVXWOLCESEKGPCEDWCRSTBSEHXFTTSTBDEHXFPYDAWVSEKSSFCTHXZNBBIPLESREUTZPDWXZALSFCGLLTBSCEEWVTONGDQSVWTYCXOHHEEZPDOYOGEAGRCZTHTNZUMVDYLRPJEOYHWPWACAPOYZXQELIRSALHPEEBGWLRWZNEOUSGPAEWOPDBBISILKDCLWOCOQNWRVLRRTREGSGLTXGIZTASEPRYSREIWSPWSNQRPEWGISEZCKPRGATYTHTISELCAOIXFPYDMVTWOOSGZFACCZUKHWTSTUPTNWSRWIGWCRIGHDOEFCRCAVMPYDWSBZCKORJIGHDEYKOCYYBBPYIFOVTNTFNMUMFTRUEOGZRWSGSAOWCRNHHBFCAFTDEFPALNVSIZTASPNTNOAQAVHHHHXBISEPVTPLAOHNOFSUFLEQXCCESLPDHBDEBXUXYAZOXYWBHWLNXKEPRBCSZFAIBLNEWUPBNHLPHTJTAALGTOFKCBEHXPTDTMCISEPCGDTTBSEHXFTHEXBSEHXGJMJXQITSMVTYCAOCREWOCOTASDWDJIPCRXZDQPHSICYTBSAHBZDDOIVNHHBQWSAWPTPNFCGPLBUWELRHGPAMSSTNMVTPAKZXPRUCDVSHTISEKSEFBEWRTSGCLCELIBPDTBSQONUWEONHIZAVCCNLNGXZNICTERRWHOILQDGEKSSEOUSPYIFWILTBCCEHKWRPRXADGEWTGZMMVTERNHWLNWVDXEKOHHEEZPDTASSCAFOITCICTESAOKTNZPTPNVCCOEFBTOALOCTMBHPEOKWHDEGHXYTHPPYILVBPNMOAZNZKXEHMVTXAGRISEBRTLOYHWPSMOIPILGJAPESBPNMSSMYMVTCEOSALTBCCZFTTJEUKSATFXHWPDBJXDIHBXYTHPDZKLZXVETZADIFWALRWWKTSBCCDCIGXCGVZTHILWCEHXQALSLWRLLFIHPUFWHARHPPMLRZPEEKHWLNMVTLGXCUALTHDEHXBPEUKOAOIOWHTOGGPCEYWKPIGBJXBXFQZODWPYDMVTQIKGISAETDQBHCZTIWCLYTHHWPPTFPRRTDWMEZWCYIGUXSAWOAHARGPOMBFTOTASVPNBIHZFZZPFCHBPYDTRTTMTBIFSPVXNHBGXYTKCSFCMCGJTASUTRLHQZODQDYTTWCTNZOGPFNHPEIHBDQTASEZPNZPCAGRHZPAWHEIVOAYOMWDYSHTYFSMWRPAGRRZNVZJOIGUATKXGDXEHTISEXOGWIXFSTAECVFELKXEHHIILRKWKTNZOILNRRTQIGWIPRXGJWTMCISILWHLPISCOEWOGPSMOIPMXBIZFMVTYAMIGPOYXJDTBQTLCVCGOIGUIZCHABZNHDXYIHBPYDTBPYSPSGTSWSBLNWSSEOMVTBUXGITOGKWLTBGYFSMWRPSMFXAPXRDQAIDTLRTBRPSMVTDEVCCODBJXDIHBXYCEISPSMVTCEFOXYDXFDQTASHPCHBSLNWHWPWACAPOYHWPTAWGOAGRUZUKHWMOHYHHHBQWLRXAPTNEMDNCNDXPDPWISTASRZNLHGFCMWDYOYHWPFBFHESMOIPAGRISEYWGDTXRJNAMWDYTASISIKRSTVBGXZNVCCDILHHZFMVTQIYHWDIQHWLNWGTGEGHWMOHYHTNPVXNHIVXWOLCESYKOISEKHWLNCIHEIVSXDTASHFBCSREOYSCBUBFNLNWHWPSXQDYDLHPEEBGRZNLHGFCMSSZNIFXYCBDAPSHTRZMFICTSFOCORNZTOBRDWTLHGDAHXFHLNWHWPCHBIPMIZPEIHBDQTASXOETCUROHRILKXGISEIZPNEHTISELCRTAEOCOPHZXEIVOAGIKHJPSBBISEXWVSTAOCONBBISBHCZDTASEPROSGDIHBHZFLHPEELOCOOYHWPIGRXGIWIPWSPVDNOKFTDPHBSEOMVTXAKSGPVBSLPDBBHFCVSHDIHBPYDMVTYAMIGPOYDAPALIGPAGRISEIFXYCBDAPOYHNCAGBNLRXTJCTASGLNTZNDEWWCEHXWCOIOWSFAEAPYTASIPNMVQZODWHEHXQDYCEIHTOGCUEHXKWZLXWCHHBQWEHXFTWAMWDYSHTESIECHZPAMIZPHSICYTFTQIGOAWYWSIPRFWCPDTBSEHXVPAPBBTDSHTISEVWITZXBHTNMVXDLBTTHHBQWSALBDHBXSCLSLIGPDBGRCOPBTOBRHWPVBGXZNHTPYOMVTCOKOBZRXUTYEKOAOIOWHTOGWCEOMKDAAKHHXARPTLDHDIPDMVTQIKGIMOHYHTIOQDYTTWCTNZHWPDXGRCIIHXZNHTPDTTHTQRTATOGXBTCAEZNTNTQRZRWOCNEPWISHXZAPNBQCZTBCCDOYFTWIZWDYAGRBZRTZXEYPVXWEBBISELSRZNWPDZKLJMEHXVTWLXBXNSMOIPILHGLNLTDCMXRXYTHOCTDXOAVIGUSZMHTESIECHZPAMDQWAWRSAEZDEHXFVZVXFCXEGHHLRXHWPPXFKPRLWDYSMVTDEMKDAOBBIDOYJXPWTFTCETZAJOIDDDEWOCOTASDAPHGXEIHBXDOGZNGEBZTOBRHWPGXBXFSHTEWAMCISEKSEFBEWRWIDSISEIVPPDKIHDEXWCERHRJNTBCCEOIVPPDKIHTSTBXXPXFUPCMKWZLXHWPHBUWPREWVSTHTESIECHZPAMQCETYHEHKCJRHMVTCEZIALRBHNZFMVTSEEZTYIVHTXPESLSIVVPELTGIQAWSHLWTMXYTHHWPHXOKPNLKWPTASGEHBGXXPXFUPCMWDYOYGICUVHJCETFXDELTGZMTBTYLTFVPMXBIZFMVTALTBDCFKCBEHXWBAEKTTNTKSRZNVWAPMXBITNMVTHRBHTCSHKCXIGRDQTASHERNUVWIGUTWEFSCESHTISONUWEWAWRSAKSCZWYWGDTUFDFGAHIZGXHWPRUMWTMHFEPRAOEDFKCBEHXQDXPHGXEIHBDQTASLZRDOIOIYTTCEGHITMXGPCEJITDTBCCDLBYTEHXGXXIEOGBUXGITOGOQZUMHWPIEWPOAGRISEHRNDSXMLSIVVPCEPCGEHTGZTNZPJEWAWRSCTBCZTAOKPAWWHEIGQILNLKTCIGHWPAZSDQPEOIZTASGPWTGCZRXUJWAKADOEHTEFBEWRLTBCCLNWOCLUMVDCWHIAOHTJTEHXZTDSLQGFPESXYAEHTCIGUDCAWRXYGMCPHOKYLSIVVLLSDBDHNHBAJTHOUPWHTWTSYFXPNWGISEKSXDNHOQDUKRXEYBBHFPICHTNZHWLTASBLYAOKPLTWSSILZPMONFHLSBRTQOKOITMXCGEUKBTOFKCBZNXKDCKMCPYOMVTCAGRHFCAWCEEKFJATBCCDWHIAOBXADCEEWZPLRHDZCVIGTNMVTNALSDQAECCRTAOCZFTGWZRMKGTTBBVTNTZALTMSBATLHDOEMSGXIGSISEVVGZNHZDRIVOAZRWSGZFMVTALTHDYIVKGTTBBVDOGWCEEKBPWEOWSPNVSISILICNEKHPTNMMPMONHPYYLWCRLXRXLLHUJPBXWCRCHAEZSXRPEOGSITMXWHLDBGIFRUWCREESBPNMKWTCAAJDTUSPOMBHIPDMCPQFXQIWOGUTCWHFZDSNQWLSMVTCEIIQWIVOCOTASALWLADCEMVPYSACGEEKCCPSUIIZNMVTZTASGSAGRISELSTXIGUSTSVFTAAGQXPSHTISEKSEFBEWRXARCCWYTFXDEHIIZFMVTOILQDCDTBIPLXATYTLKWTCAHWPPAWAZSHDWPRAOHLTMSBATXRIZUGWIPIGOHTNZZTHHHZTAEKVPASPWISONHQPIGUWTMLSAQAUZTEOKSRZGGWHPTASXYCHBHTSMSCNYPVXNHBGDMVBCJDTHIHQOKHWPRXWHLJNRVXEGHDQAYHTCAZSHHHBQWQEPUGPAMKGTTXFHSAOSTGEKPTPNTPAPTHOCEIVWELTXTDCTASBDEEJTDTASNOOGCIAEKQTTVXHWPWTBIZFVCCYEQWDYIGHWPIKCLYWKWITNZGDCTASVLPLWCEHXWGDYLHTXSPVXNHTFTGILWQWEXBDFGAHDEHHGTHHHQDXETTIPRMVTXIGHWPBXUXYNBBVDOYZXEEKOIFRXOCOPAWAZSHDWJAFWSEHXTXCSMSUQOKHHZFMVDFGAHPYDEOCRUTUTXOKSXYCHBHTSMSCNIXGDNCNFISAGBDHWASCEHXDPEHLCUDPXQJWAMWDYAKSLPLEKDCNTBSEHXATLNBBVZFPCGOSIFTNILSAJDXTXYEWTDCCHBHTSMSCNYMCDTSMVTRRHKISOYHXXETBSDOFSDQTASVCETHTDTVFTLTBCCDOYHWPHNAPYMBBSSAOSQPEGKPYTBBVTNNBXEYMFXPDUMISILHTDTLSKPRTZDQTASEWAMCCTCWWPWOZITDAVQDCDBBVEOHIGXOWSGYIWSPDAIDTLRMCQPDXTTNTBJTMUMHWPDXTXNIXBRJILBDARHCUEHTHISERKTCEVCBAOLSSLTWWUQEKSCETBATDOKPNOIYTTCEGHWLNWGPYDMVTDUIDDDIMWDYTAOIEHXFTAUUZXNWTGLCIMHTYUGWCEEKFJATXRAJAGRQJAVCCEIGIDFSXTUZRMWHTNLCBPDXUGPEVCCQIKATOBRHWPNNATCONGGPFXFTYCXGUCOFCCPPTFIZFMVTHOKYIZAGCISEK"""        
        print "friedman: ",friedman(cyphertext)#4.30271679085
        print "find_best_key_len: ",find_best_key_len(cyphertext)#5
        print "move_letters_according_to_key_len: (Key,Text) = ",move_letters_according_to_key_len(cyphertext, 5)
        self.assertTrue(True)
        
if __name__ == '__main__':
    unittest.main()
