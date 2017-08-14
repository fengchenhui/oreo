import os.path
file_output=open('output/Method_Token_Map.txt', 'w')
file_notokens=open('output/MethodNoToken.txt', 'w')
dictmethods=dict()
notokens=0
with open('input/IjaMapping_new_uniquetokens.txt','r') as file_input:
    for line in file_input:
        line_splitted=line.replace('\n','').replace('\r','').split(':')
        fqmn=line_splitted[0]
        file_info=line_splitted[1].split(',')
        dir_name=file_info[0]
        file_name = file_info[1]
        startline = int(file_info[2])
        endline = int(file_info[3])
        i=0
        if os.path.isfile(dir_name+'/'+file_name):
            print(dir_name+'/'+file_name)
            with open(dir_name+'/'+file_name) as file:
                tokenseen=False
                tokens=dict()
                for line_code in file:
                    methodname = ''
                    fieldname = ''
                    token=''
                    i+=1
                    commentSeen=False
                    if i>=startline and i<=endline:
                        for c in line_code:
                            if c=='"' and not commentSeen:
                                commentSeen=True
                                continue
                            if c=='"' and commentSeen:
                                commentSeen=False
                                continue
                            if not commentSeen:
                                if c=='(' and tokenseen:
                                    if token+'()' in tokens:
                                        tokens[token+'()']+=1
                                    else:
                                        tokens[token+'()']=1
                                    tokenseen = False
                                    token=''
                                    continue
                                if c!='(' and c!='_' and c!='$' and not c.isalnum() and c!='.' and tokenseen:
                                    if token in tokens:
                                        tokens[token]+=1
                                    else:
                                        tokens[token]=1
                                    tokenseen = False
                                    token=''
                                    continue
                                if tokenseen:
                                    token+=c
                                if c=='.':
                                    token=''
                                    tokenseen=True
                    elif i > endline:
                        break
            if len(tokens)>0:
                dictmethods[fqmn] = tokens
            else:
                notokens+=1
                file_notokens.write(fqmn+'\n')
            file.close()
print('begin writing..')
print('number of methods having no tokens: '+str(notokens))
for key,value in dictmethods.items():
    linetowrite=key+'@#@'
    for token in value.keys():
        linetowrite+=token+':'+str(value[token])+','
    linetowrite=linetowrite[:-1]
    file_output.write(linetowrite+'\n')
    linetowrite=''
file_output.close()
file_notokens.close()