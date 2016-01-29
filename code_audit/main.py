#coding=utf-8
'''
@author: K1n9
'''
import os
import cgi
import sys

def f_list(rootdir):
    files = set()
    files_list = set()
    
    for parent,dirnames,filenames in os.walk(rootdir):#dirnames @UnusedVariable
        for filename in filenames:
            files.add(os.path.join(parent,filename))
    for val in files:
        if val[-4:].lower() == '.php':
            files_list.add(val)
    
    return files_list


def f_search(files_list,str_list):
    lines_dic = {}

    for filename in files_list:
        lines_cont = set()
        f = open(filename,'r')
        file_content = f.read()
        f.close()
        for val in str_list:
            if val in file_content.lower():
                f2 = open(filename,'r')
                cont = f2.readline()
                while cont != '':
                    if val in cont.lower():
                        lines_cont.add(cont.strip('\n').strip('\t'))
                    cont = f2.readline()
                f2.close()
        if len(lines_cont) != 0:
            lines_dic[filename] = lines_cont

    return lines_dic


def output_html_all(output_list):
    fout = open('all_output.html','w')
    fout.write('<html>')
    fout.write('<body>')
    fout.write('<h4>parameter:</h4>')
    output_table(fout,output_list[0])
    fout.write('<h4>Sql:</h4>')
    output_table(fout,output_list[1])
    fout.write('<h4>Include:</h4>')
    output_table(fout,output_list[2])
    fout.write('<h4>Execute:</h4>')
    output_table(fout,output_list[3])
    fout.write('<h4>Output:</h4>')
    output_table(fout,output_list[4])
    fout.write('<h4>File:</h4>')
    output_table(fout,output_list[5])
    fout.write('</body>')
    fout.write('</html>')
    print 'Output finished'
    fout.close()


def output_html_one(output_list):
    fout = open('one_output.html','w')
    fout.write('<html>')
    fout.write('<body>')
    fout.write('<h4>%s:</h4>' % sys.argv[2])
    output_table(fout,output_list[0])
    fout.write('</body>')
    fout.write('</html>')
    print 'Output finished'
    fout.close()


def output_table(fout,output):
    if len(output) == 0:
        fout.write('<table width="100%" border="1">')
        fout.write('<th>Not found</th>')
        fout.write('</table>')
    else:
        fout.write('<table width="100%" border="1">')
        for k in output:
            for val in output[k]:
                fout.write('<tr>')
                fout.write('<td width="50%">'+'%s</td>' % k)
                fout.write('<td width="50%">'+'%s</td>' % cgi.escape(val))
                fout.write('</tr>')
        fout.write('</table>')


if __name__ == "__main__":
    parameter  = ['$_get','$_post','$_cookie','$_request','$_files']
    sql = ['sql','select','insert','update','delete','from','where','limit']
    include = ['include','require','include_once','require_once']
    execute = ['eval','assert']
    output = ['echo','print']
    files = ['file_get_contents','file_put_contents']
    keyword_list = [parameter,sql,include,execute,output,files]
    
    rootdir = sys.argv[1]
  
    files_list = f_list(rootdir)

    output_list = []
    if len(sys.argv) == 2:
        for val in keyword_list:
            output_list.append(f_search(files_list,val))
        output_html_all(output_list)
    else:
        keyword = [sys.argv[2]]
        output_list.append(f_search(files_list,keyword))
        output_html_one(output_list)
