import csv, os, collections, shutil
print(
        'Aloha Daily Status Report Generator V1.1 by Bernard'
        +'\n- Compatible with PayApp V1.9.11'
        +'\n- Please save the script and .csv file in same folder, a text file report will be generated in the same folder'
        +'\n- The .csv file information must be correct in order to generate the report, manually correct the .csv if have to '
        +'\n- Store names, address, device type, serial number, SW need to match, sometimes address for same store maybe'
        +'\nchanged during payapp entry, please correct them into one same address'
        +'\n- Use period instead of comma in failed comment. Enter the reader info in Product Item Details on payapp'
        +'\n- Known issues:'
)

file_name = input('Please copy/paste full .csv file path: \n')

with open(file_name, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    reader_list = []
    for row in reader:
        reader_list.append(row)


def tested_locations():
    location_list = []
    for row in reader_list:
        row_str = row[0] + ': ' + row[1]
        if row_str not in location_list:
            location_list.append(row_str)
    location_list.pop(0)
    location_list.pop(0)
    # for i in location_list: print(i)
    report_file = open('report.txt','w')
    report_file.write('From '+ file_name + '\n\nTested Locations:\n')
    if len(location_list) == 0:
        report_file.write('-N/A\n')
    elif len(location_list) != 0:
        for i in location_list:
            report_file.write('-'+i+'\n')
    report_file.close()


def tap_not_allowed():
    location_list = []
    for row in reader_list:
        row_str = row[0] + ':' + row[1] + ': ' + row[18]
        if row[7] == 'FAIL' and 'tap not allowed' in row[26] and row[6] != 'Discover':
            location_list.append(row_str)
    report_file = open('report.txt','a')
    report_file.write('\nTap not allowed: \n')
    # for i in location_list: print(i)
    if len(location_list) == 0:
        report_file.write('-N/A\n')
    elif len(location_list) != 0:
        for i in location_list:
            report_file.write('-'+i+'\n')
    report_file.close()


def card_not_accepted():
    location_list = []
    for row in reader_list:
        row_str = row[0] + ': ' + row[1] + ': ' + row[18]
        if row[7] == 'FAIL' and 'not accepted' in row[26] and row[6] != 'Discover':
            location_list.append(row_str)
    # for i in location_list: print(i)
    report_file = open('report.txt','a')
    report_file.write('\nCard not accepted:\n')
    if len(location_list) == 0:
        report_file.write('-N/A\n')
    elif len(location_list) != 0:
        for i in location_list:
            report_file.write('-'+i+'\n')
    report_file.close()


def refunds():
    refund_list = []
    for row in reader_list:
        row_str = row[0] + ': ' + row[1] + ': ' + row[18]
        if str(row[24]) == 'YES':
            refund_list.append(row_str)
    # for i in refund_list:print(i)
    report_file = open('report.txt','a')
    report_file.write('\nRefunds:\n')
    if len(refund_list) == 0:
        report_file.write('-N/A\n')
    elif len(refund_list) != 0:
        for i in refund_list:
            report_file.write('-'+i+'\n')
    report_file.close()


def technology_not_available():
    tna_list = []
    for row in reader_list:
        row_str = row[0] + ': ' + row[1]
        if row[14] == 'NO' and ('tap' in row[26] or 'Tap' in row[26]):
            tna_list.append(row_str)
    # for i in tna_list:print(i)
    report_file = open('report.txt','a')
    report_file.write('\nTechnology Not Available:')
    if len(tna_list) == 0:
        report_file.write('\n-N/A\n')
    elif len(tna_list) != 0:
        for i in tna_list:
            report_file.write('\n'+'-'+i)
    report_file.close()


def location_not_available():
    tna_list = []
    for row in reader_list:
        row_str = row[0] + ': ' + row[1]
        if row[14] == 'NO' and ('location' in row[26] or 'Location' in row[26]):
            tna_list.append(row_str)
    # for i in tna_list:print(i)
    report_file = open('report.txt','a')
    report_file.write('\n\nLocation Not Available:')
    if len(tna_list) == 0:
        report_file.write('\n-N/A\n')
    elif len(tna_list) != 0:
        for i in tna_list:
            report_file.write('\n'+'-'+i)
    report_file.close()


def no_issue():
    location_list = []
    verdict_list = []
    location_address_list = []
    for row in reader_list:
        location_list.append(row[0])  # store names
        location_address_list.append(row[0] + ': ' + row[1])  # store names + address
        verdict_list.append(row[7])
    location_list.pop(0)
    location_list.pop(0)
    location_address_list.pop(0)
    location_address_list.pop(0)
    verdict_list.pop(0)
    verdict_list.pop(0)
    # print(location_address_list)
    index_list =[]
    for i in get_duplicates_item_index(location_list):  # get the dictionary with store name as key and duplicates index as value
        # print(get_duplicates_item_index(location_list)[i])
        index_list.append(get_duplicates_item_index(location_list)[i])  # extract the duplicates index as list of list
    # print('list index\n',index_list)
    no_issue_list = []
    for item in index_list:  # find out if all duplicates have pass verdict
        pass_counter = 0
        for i in item:
            if verdict_list[i] == 'PASS':
                pass_counter += 1
            else: pass
        # print('pass counter',pass_counter)
        if pass_counter == len(item):
            for i in item:
                no_issue_list.append(location_address_list[i])
                break
        else: pass
    # for i in no_issue_list: print(i)
    report_file = open('report.txt','a')
    report_file.write('\nNo Issues (All Cards):\n')
    for i in no_issue_list:
        report_file.write('-'+i+'\n')
    report_file.close()


def get_duplicates_item_index(n):
    counter = collections.Counter(n)
    dups = [i for i in counter]
    result = {}
    for item in dups:
        result[item] = [i for i,j in enumerate(n) if j==item]
    return result


def device_issue():  # can not loop the same iterator twice
    report_file = open('report.txt','a')
    report_file.write('\n\nDevice Issues:\n')
    for row in reader_list:
        if row[7] == 'FAIL' and row[16] == 'PASS' and row[6] != 'Discover':
            report_file.write('\n'+ row[0]+ ':'+ row[1]+'\n')
            report_file.write(row[6]+' '+row[18]+ 'FPAN:'+ row[17]+ '; '+ 'DPAN:'+ row[21]+ '- Fail\n')
            report_file.write(row[26]+'\n')
            report_file.write('Date/Time:'+row[3]+'/'+row[4]+'\n')
            report_file.write('Amount:'+row[22]+'\n')
            report_file.write('Currency/Amount shown in passbook history: Yes\n')
            fail_comment = row[26].split('.')
            for i in fail_comment:
                if 'reader'in i or 'Reader' in i:
                    report_file.write('POS Reader:'+i+'\n')
            for i in fail_comment:
                if 'dut' in i or 'DUT' in i:
                    report_file.write('DUT Display:'+i+'\n')
            report_file.write('Radar Link: \n')
            report_file.write('Card - Multiple Attempts'+ '\nAll 3 attempts results in same observation.\n')
            report_file.write('Other cards failed: ')
            l1 = get_other_failed_cards(row)
            if len(l1) == 0:
                report_file.write('N/A\n')
            else:
                for i in l1: report_file.write(i[1]+' '+i[2]+' '+'FPAN:'+i[3]+' '+'DPAN:'+i[4]+'; ')
            l2 = get_other_passed_cards(row)
            report_file.write('\nOther cards passed: ')
            if len(l2) == 0:
                report_file.write('N/A')
            else:
                for i in l2: report_file.write(i[1]+' '+i[2]+' '+'FPAN:'+i[3]+' '+'DPAN:'+i[4]+'; ')
            report_file.write('Ref Card: '+row[15]+'\n')

        elif row[7] == 'FAIL' and row[6] == 'Discover' and row[14] == 'YES':
            report_file.write('\n'+ row[0]+ ':'+ row[1]+'\n')
            report_file.write(row[6]+' FPAN:'+ row[17]+ '; '+ 'DPAN:'+ row[21]+ ' - Fail\n')
            report_file.write(row[26]+'\n')
            report_file.write('Date/Time:'+row[3]+'/'+row[4]+'\n')
            report_file.write('Amount:'+row[22]+'\n')
            report_file.write('Currency/Amount shown in passbook history: Yes\n')
            fail_comment = row[26].split('.')
            for i in fail_comment:
                if 'reader'in i or 'Reader' in i:
                    report_file.write('POS Reader:'+i+'\n')
            for i in fail_comment:
                if 'dut' in i or 'DUT' in i:
                    report_file.write('DUT Display:'+i+'\n')
            report_file.write('Radar Link: \n')
            report_file.write('Card - Multiple Attempts'+ '\nAll 3 attempts results in same observation.\n')
            report_file.write('Other cards failed: ')
            l1 = get_other_failed_cards(row)
            if len(l1) == 0:
                report_file.write('N/A')
            else:
                for i in l1: report_file.write(i[1]+' '+i[2]+' '+'FPAN:'+i[3]+' '+'DPAN:'+i[4]+'; ')
            l2 = get_other_passed_cards(row)
            report_file.write('\nOther cards passed: ')
            if len(l2) == 0:
                report_file.write('N/A')
            else:
                for i in l2: report_file.write(i[1]+' '+i[2]+' '+'FPAN:'+i[3]+' '+'DPAN:'+i[4]+'; ')
            report_file.write('\n')
    report_file.close()


def get_other_failed_cards(list_row):
    failed_cards_list = []
    for row in reader_list:
        failed_card = []
        if row[7] == 'FAIL' and row[16] == 'PASS' and row[6] != 'Discover':
            failed_card.append(row[0])
            failed_card.append(row[6])
            failed_card.append(row[18])
            failed_card.append(row[17])
            failed_card.append(row[21])
            failed_card.append(row[1])
            failed_cards_list.append(failed_card)
        elif row[7] == 'FAIL' and row[6] == 'Discover':
            failed_card.append(row[0])
            failed_card.append(row[6])
            failed_card.append(row[18])
            failed_card.append(row[17])
            failed_card.append(row[21])
            failed_card.append(row[1])
            failed_cards_list.append(failed_card)
    other_failed_cards = []
    for i in failed_cards_list:
        if i[0] == list_row[0] and i[4] != list_row[21] and i[5] == list_row[1]:
            other_failed_cards.append(i)
    return other_failed_cards


def get_other_passed_cards(list_row):
    passed_cards_list = []
    for row in reader_list:
        passed_card = []
        if row[7] == 'PASS':
            passed_card.append(row[0])
            passed_card.append(row[6])
            passed_card.append(row[18])
            passed_card.append(row[17])
            passed_card.append(row[21])
            passed_card.append(row[1])
            passed_cards_list.append(passed_card)
        else: pass
    other_passed_cards = []
    for i in passed_cards_list:
        if i[0] == list_row[0] and i[4] != list_row[21] and i[5] == list_row[1]:
            other_passed_cards.append(i)
    return other_passed_cards


def get_failed_stores_info():
    failed_store_names = []
    for row in reader_list:
        if row[7] == 'FAIL' and row[16] == 'PASS' and row[0] not in failed_store_names and row[0] != 'Discover':
            failed_store_names.append(row[0])
        elif row[7] == 'FAIL' and row[6] == 'Discover'and row[14] == 'YES' and row[0] not in failed_store_names:
            failed_store_names.append(row[0])
    # for i in failed_store_names: print(i)
    failed_stores_info = []
    for row in reader_list:
        failed_stores_info_temp = []
        if row[0] in failed_store_names:
            failed_stores_info_temp.append(row[0])
            failed_stores_info_temp.append(row[6])
            failed_stores_info_temp.append(row[18])
            failed_stores_info_temp.append(row[17])
            failed_stores_info_temp.append(row[21])
            failed_stores_info_temp.append(row[5])
            failed_stores_info_temp.append(row[1])
            failed_stores_info.append(failed_stores_info_temp)
    # for i in failed_stores_info: print(i)
    return failed_stores_info


def failures():
    report_file = open('report.txt','a')
    report_file.write('\nFailures:\n')
    fsi = get_failed_stores_info()
    for row in reader_list:
        if row[7] == 'FAIL' and row[16] == 'PASS' and row[6] != 'Discover':
            report_file.write('\n[Field Test-P3]'+'['+row[38]+'-'+row[2]+']['+row[6]+']['+row[18]+']['+row[0]+']'+row[26]+'\n')
            report_file.write('* SUMMARY\n'+row[26]+
                              '\n* STEPS TO REPRODUCE\nOrientation: Any\nRange: Any\n1.Tap Phone\n2.Select Card\n3.Tap device on reader'+
                            '\n\nTransaction Details:\n')
            report_file.write(row[5]+'-'+row[11]+'\nSW: '+row[23]+'\nDate/Time: '+row[3]+'/'+row[4]+'\nAmount: '+row[22]+
                              '\nCurrency/Amount shown in passbook history: '+row[37]+
                              '\nDPAN: '+row[21]+'\nFPAN: '+row[17]+'\nPNO: '+ row[18]+'\nBANK: '+row[6]+
                              '\nAddress: '+ row[1]+'\nStore Name: '+row[0]+'\nReader Info: '+row[28]+
                              '\nOther cards failed: ')
            l1 = get_other_failed_cards(row)
            if len(l1) == 0:
                report_file.write('N/A\n')
            else:
                for i in l1: report_file.write(i[1]+' '+i[2]+' '+'FPAN:'+i[3]+' '+'DPAN:'+i[4]+'; ')
            l2 = get_other_passed_cards(row)
            report_file.write('\nOther cards passed: ')
            if len(l2) == 0:
                report_file.write('N/A')
            else:
                for i in l2: report_file.write(i[1]+' '+i[2]+' '+'FPAN:'+i[3]+' '+'DPAN:'+i[4]+'; ')
            report_file.write('Ref Card: '+row[15])
            report_file.write('\nOrder of cards tested at location:\n')

            for i in fsi:
                if row[0] in i:
                    report_file.write('-'+i[5]+': '+i[1]+' '+i[2]+' FPAN: '+i[3]+' DPAN: '+i[4]+';\n')
                else: pass

        elif row[7] == 'FAIL' and row[6] == 'Discover' and row[14] == 'YES':
            report_file.write('\n[Field Test-P3]'+'['+row[38]+'-'+row[2]+']['+row[6]+']['+row[18]+']['+row[0]+']'+row[26]+'\n')
            report_file.write('* SUMMARY\n'+row[26]+
                              '\n* STEPS TO REPRODUCE\nOrientation: Any\nRange: Any\n1.Tap Phone\n2.Select Card\n3.Tap device on reader'+
                            '\n\nTransaction Details:\n')
            report_file.write(row[5]+'-'+row[11]+'\nSW: '+row[23]+'\nDate/Time: '+row[3]+'/'+row[4]+'\nAmount: '+row[22]+
                              '\nCurrency/Amount shown in passbook history: '+row[37]+
                              '\nDPAN: '+row[21]+'\nFPAN: '+row[17]+'\nPNO: '+ row[18]+'\nBANK: '+row[6]+
                              '\nAddress: '+ row[1]+'\nStore Name: '+row[0]+'\nReader Info: '+row[28]+
                              '\nOther cards failed: ')
            l1 = get_other_failed_cards(row)
            if len(l1) == 0:
                report_file.write('N/A')
            else:
                for i in l1: report_file.write(i[1]+' '+i[2]+' '+'FPAN:'+i[3]+' '+'DPAN:'+i[4]+'; ')
            l2 = get_other_passed_cards(row)
            report_file.write('\nOther cards passed: ')
            if len(l2) == 0:
                report_file.write('N/A')
            else:
                for i in l2: report_file.write(i[1]+' '+i[2]+' '+'FPAN:'+i[3]+' '+'DPAN:'+i[4]+'; ')
            report_file.write('\nOrder of cards tested at location:\n')

            for i in fsi:
                if row[0] in i and row[1] in i:
                    report_file.write('-'+i[5]+': '+i[1]+' '+i[2]+' FPAN: '+i[3]+' DPAN: '+i[4]+';\n')
                else: pass
    report_file.close()

tested_locations()
tap_not_allowed()
card_not_accepted()
refunds()
no_issue()
technology_not_available()
location_not_available()
device_issue()
failures()
print('Report is saved in the same folder as the .exe file')
input('press enter to quit')