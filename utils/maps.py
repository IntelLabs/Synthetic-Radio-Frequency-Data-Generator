mod_str2int = {"awgn":(0,"awgn"),
               "bpsk":(1,2,1,"bpsk"), "qpsk":(1,4,2,"qpsk"), "8psk":(1,8,3,"8psk"), 
               "16psk":(1,16,4,"16psk"), "32psk":(1,32,5,"32psk"), "64psk":(1,64,6,"64psk"),
               "128psk":(1,128,7,"128psk"), "256psk":(1,256,8,"256psk"), 
               "4qam":(2,4,2,"4qam"), "8qam":(2,8,3,"8qam"), "16qam":(2,16,4,"16qam"), 
               "32qam":(2,32,5,"32qam"), "64qam":(2,64,6,"64qam"), "128qam":(2,128,7,"128qam"), 
               "256qam":(2,256,8,"256qam"),
               "2ask":(3,2,1,"2ask"), "4ask":(3,4,2,"4ask"), "8ask":(3,8,3,"8ask"), 
               "16ask":(3,16,4,"16ask"), "32ask":(3,32,5,"32ask"), "64ask":(3,64,6,"64ask"), 
               "128ask":(3,128,7,"128ask"), "256ask":(3,256,8,"256ask"), 
               "2apsk":(4,2,1,"2apsk"), "4apsk":(4,4,2,"4apsk"), "8apsk":(4,8,3,"8apsk"), 
               "16apsk":(4,16,4,"16apsk"), "32apsk":(4,32,5,"32apsk"), "64apsk":(4,64,6,"64apsk"), 
               "128apsk":(4,128,7,"128apsk"), "256apsk":(4,256,8,"256apsk"),
               "2dpsk":(5,2,1,"2dpsk"), "4dpsk":(5,4,2,"4dpsk"), "8dpsk":(5,8,3,"8dpsk"), 
               "16dpsk":(5,16,4,"16dpsk"), "32dpsk":(5,32,5,"32dpsk"), "64dpsk":(5,64,6,"64dpsk"), 
               "128dpsk":(5,128,7,"128dpsk"), "256dpsk":(5,256,8,"256dpsk"),
               "dsb":(6,0,"dsb"),
               "dsbsc":(6,1,"dsbsc"), 
               "usb":(6,2,"usb"), 
               "lsb":(6,3,"lsb"), 
               "fmnb":(7,0,"fmnb"), 
               "fmwb":(7,1,"fmwb"), 
               "fsk5k":(8,2,1.0,0,"fsk5k"), # 5k, square pulse shape
               "fsk75k":(8,2,15.0,0,"fsk75k"), # 75k, square pulse shape
               "gfsk5k":(8,2,1.0,1,"gfsk5k"), # 5k, gauss pulse shape
               "gfsk75k":(8,2,15.0,1,"gfsk75k"), # 75k, gauss pulse shape
               "msk":(8,2,0.5,0,"msk"), # 2.5k, square pulse shape
               "gmsk":(8,2,0.5,1,"gmsk")} # 2.5k, gauss pulse shape
               
mod_int2type = {0:"none", 1:"digital", 2:"digital", 3:"analog", 4:"digital", 
                5:"digital", 6:"analog", 7:"analog", 8:"digital"}

mod_int2modem = {0:None, 1:"linear", 2:"linear", 3:"linear", 4:"linear", 
                 5:"linear", 6:"amplitude", 7:"frequency", 8:"freq_shift"}

mod_int2class = {0: "awgn", 1:"psk", 2:"qam", 3:"ask", 4:"apsk", 5:"dpsk", 
                 6:"am", 7:"fm", 8:"fsk"}

mod_int2symbolvariant = {0:None, 1:None, 2:None, 3:None, 4:None, 5:"differential",
                         6:None, 7:None, 8:None}

am_variants = {0:"dsb", 1:"dsbsc", 2:"usb", 3:"lsb"}

fm_variants = {0:"nb", 1:"wb"}