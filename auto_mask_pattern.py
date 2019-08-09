import re
import time
def mask_process(fail_log_name, fail_pattern_name, modify_pattern_name):
    start = time.clock()
#    fail_log_name='C:/Python Training/test/ac_scan_fail_loop.txt'
    print('Fail log is:%s .\n'%fail_log_name)
    fail_log=open(fail_log_name,'r')
    log_line=fail_log.readlines()
    pins_row=0
    pins_flag=[]
    for eachline in log_line:
        if eachline.strip() == 'PINS':
            pins_flag.append(pins_row)
        pins_row=pins_row+1
    #print(pins_flag)
    log_split=[]
    if(len(pins_flag)==1):
        log_split.append(log_line)
    else:
        for i in range(0,len(pins_flag)-1):
            log_split.append(log_line[pins_flag[i]-1:pins_flag[i+1]-1])
    modify_pins=[]
    modify_value=[]
    modify_pins_name=[]
    for i in range(0,len(log_split)):
        temp=pick_modify_data(log_split[i])
        modify_pins.append(temp[0])
        modify_value.append(temp[1])
        modify_pins_name.extend(temp[0])
    modify_pins_name=list(set(modify_pins_name))
    modify_pins_cnt=len(modify_pins_name)
    print('Modify pin count: %d.'%modify_pins_cnt)
    print('Modify pin name: %s .'%modify_pins_name)
    print('-------------------------------------------------------')
    #print(modify_value)
    modify_rows=[]
    for i in range(0,len(log_split)):
        for j in range(0,len(modify_value[i])):
            modify_rows.append(modify_value[i][j][0])
    #print(modify_rows)
    modify_set=set(modify_rows)
    modify_rows_ur=[i for i in modify_set]
    #print(modify_rows_ur)
    modify_value_lp=[[0,'']for i in range(len(modify_rows_ur))]
    for i in range(0,len(log_split)):
        for j in range(0,len(modify_value[i])):
            for k in range(0,len(modify_rows_ur)):
                if modify_value[i][j][0] == modify_rows_ur[k]:
                    modify_value_lp[k][0] = modify_value[i][j][0];
                    if modify_value_lp[k][1]=='':
                        for p in range(0, modify_pins_cnt):
                            if modify_pins_name[p] in modify_pins[i]:
                                for q in range(0, len(modify_pins[i])):
                                    if modify_pins[i][q]==modify_pins_name[p]:
                                        modify_value_lp[k][1]=modify_value_lp[k][1]+list(modify_value[i][j][1])[q]
                            else:
                                modify_value_lp[k][1]=modify_value_lp[k][1]+'V'
                    else:
                        modify_value_lp[k][1]=str_or_x(modify_value_lp[k][1],modify_value[i][j][1])
    print("Modify vector num is : %d."%len(modify_value_lp))
    print(modify_value_lp)
    #fail_pattern_name=input('Enter fail pattern path & name: ')
#    fail_pattern_name='C:/Python Training/test/pangu_chip_top_scan_comp_lp_ac_maskX_V7.atp'
    print('Fail pattern is:%s.\n'%fail_pattern_name)
    #modify_pattern_name=input('Enter modify pattern path & name: ')
#    modify_pattern_name='C:/Python Training/test/pangu_chip_top_scan_comp_lp_ac_maskX_V8.atp'
    mask_pattern(fail_pattern_name,modify_pattern_name,modify_pins_name,modify_value_lp)
    end = time.clock()
    print (str(end-start))
    return('The program has been executed!')
    
def str_or_x(str1,str2):
    str3=''
    for i in range(0,len(str1)):
        if str1[i]=='X' or str2[i]=='X':
            str3=str3+'X'
        else:
            str3=str3+str2[i]
    return(str3)

def pick_modify_data(log_line):
    pins_row=1
    line_cnt=pins_row+1
    i=0
    pin_name_len=0
    pin_num=len(log_line[line_cnt].strip().strip('\n'))
    #print('Fail pin count: %d\n'%pin_num)
    pin_first_line=log_line[2].strip().strip('\n')
    pin_first_line_index=log_line[2].index(pin_first_line[0])
    #print(pin_first_line_index)
    pin_name=[]
    while ((log_line[line_cnt+i].strip().strip('\n') != 'CHANNELS') and (log_line[line_cnt+i] != '\n')):
        #pin_name[0]=pin_name[0]+log_line[line_cnt+i].strip().strip('\n')
        temp=log_line[line_cnt+i]
        pin_name_len=pin_name_len+1
        i=i+1
    #print(pin_name_len)
    for i in range(0,pin_name_len):
        pin_name.append(log_line[2+i][pin_first_line_index:pin_first_line_index+pin_num])
    #print(pin_name)
    pin_name_conver=[]
    pin_name_str=""
    for i in range(0,pin_num):
        for j in range(0,pin_name_len):
            pin_name_str=pin_name_str+pin_name[j][i]
        pin_name_str=pin_name_str.strip()
        pin_name_conver.append(pin_name_str)
        pin_name_str=""
    #print('Fail pin name: %s .'%pin_name_conver)
    row_cnt=0
    log_split=[]
    fail_row=[]
    for eachline in log_line:
        for item in eachline.split():
            if item == '->FAIL':
                fail_row.append(row_cnt)
        row_cnt=row_cnt+1
    #print('Fail vector number: %d.'%len(fail_row))
    fail_key=[[0 for i in range(3)]for i in range(len(fail_row))]
    for i in range(0,len(fail_row)):
        log_split=log_line[fail_row[i]-1].split()
        fail_key[i][0]=int(log_split[2])
        fail_key[i][1]=log_split[4]
        log_split=log_line[fail_row[i]].split()
        fail_key[i][2]=log_split[1]
    #print(fail_key)
    expect_str=''
    actual_str=''
    modify_str=''
    modify_value=[[0 for i in range(2)]for i in range(len(fail_row))]
    for i in range(0,len(fail_row)):
        expect_str=fail_key[i][1]
        actual_str=fail_key[i][2]
        for j in range(0,len(expect_str)):
            if expect_str[j]!='X' and expect_str[j]!=actual_str[j]:
                modify_str=modify_str+'X'
            else:
                modify_str=modify_str+expect_str[j]
        modify_value[i][0]=fail_key[i][0]
        modify_value[i][1]=modify_str
        expect_str=''
        actual_str=''
        modify_str=''
    #print(modify_value)
    return([pin_name_conver,modify_value])

def mask_pattern(fail_pattern_name,modify_pattern_name,pin_name_conver,modify_value):
    fail_pattern=open(fail_pattern_name,'r')
    modify_pattern=open(modify_pattern_name,'w')
    print('Fail pattern was opened successfully!')
    #pattern_line=fail_pattern.readlines()
    #print('Fail pattern was readed successfully!')
    pin_header=0
    pin_header_flag=0
    pin_sep=[i for i in range(0,len(pin_name_conver))]
    re_str='\s(0|1|X|L|H|M)'
    for eachline in fail_pattern:
        if pin_header_flag == 1:
            vector_flag=re.search(re_str,eachline)
            if vector_flag is not None:
                pin_col=[i.start() for i in re.finditer(re_str,eachline)]
                for i in range(0,len(pin_name_conver)):
                    for j in range(0,len(pin_list)):
                        if pin_name_conver[i] == pin_list[j].strip().strip('\n'):
                            pin_sep[i]=pin_col[j]+1
                print('Fail pin sequence are: ')
                for i in range(0,len(pin_sep)):
                    print('%s:%d  '%(pin_name_conver[i],pin_sep[i]))
                break
        if pin_header_flag != 1:
            pin_header=pin_header+1
            for item in eachline.split(','):
                if 'vector' in item:
                   pin_list=eachline.split(',')
                   pin_list[len(pin_list)-1]=pin_list[len(pin_list)-1].strip('\n').strip(')')
                   pin_list=pin_list[1:]
                   pin_header_flag=1
                   print('Pin header row is : %d.'% pin_header)
                   print('Pin list is :\n %s .'%pin_list)
    fail_pattern.seek(0,0)
    pat_row=0
    pat_col=0
    pat_value=''
    line_list=[]
    for eachline in fail_pattern:
        for i in range(0,len(modify_value)):
            if (modify_value[i][0]+pin_header+2) == pat_row:
                #print(pat_row)
                pat_value=modify_value[i][1]
                line_list=list(eachline)
                for j in range(0,len(eachline)):
                    for k in range(0,len(pin_name_conver)):
                        if (j == pin_sep[k]) and  (pat_value[k]!='V'):
                            line_list[j]=pat_value[k]
                modify_line=''.join(line_list)
                print('Init vector %d :    %s'%(modify_value[i][0],''.join(re.split('\s+',eachline.strip()))))
                print('Modify vector %d :  %s'%(modify_value[i][0],''.join(re.split('\s+',modify_line.strip()))))
                eachline=modify_line
        modify_pattern.write(eachline)
        pat_row=pat_row+1
    print(pat_row)
    fail_pattern.close()
    modify_pattern.close()

if __name__ == '__mian__':
    main()
