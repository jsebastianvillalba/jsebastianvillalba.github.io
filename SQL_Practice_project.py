#Student: Jose Sebastian Villalba
#Number: 3162433

# FINAL PROJECT

import sqlite3

conn = sqlite3.connect('employees_db-full-1.0.6.db')
cur = conn.cursor()


#What is the total head count of all current employees at Epoch systems?
cur.execute('SELECT * FROM dept_emp WHERE to_date = "9999-01-01"')

number_empleyees = 0
for row in cur:
    number_empleyees += 1
print('Number of employees: ', number_empleyees)

#What is the distribution of head count for current employees across the various departments?
cur.execute('SELECT * FROM departments')
d= dict()
for row in cur:
    d[row[0]] = row[1]
for key in d:
    cur.execute('SELECT * FROM dept_emp WHERE to_date = "9999-01-01" AND dept_no = "%s"'%key)
    n = 0
    for row in cur:
        n += 1
    print('number of employees in ', d[key],' department is:',n)
#Test that data is inconsistent

#What is the average salary of all current employees by department ?
#What is the max salary of all current employees by department?
cc = 0
for key in d:  
    #cur.execute('SELECT salaries.emp_no, salaries.salary, salaries.to_date, dept_emp.dept_no FROM salaries JOIN dept_emp  ON salaries.emp_no = dept_emp.emp_no WHERE salaries.to_date = "9999-01-01" AND dept_no = "%s"'%key )
    cur.execute('SELECT salaries.emp_no, salaries.salary, salaries.to_date, dept_emp.dept_no FROM salaries JOIN dept_emp  ON salaries.emp_no = dept_emp.emp_no WHERE salaries.to_date = "9999-01-01" AND dept_emp.to_date = "9999-01-01" AND dept_no = "%s" '%key)
    tot_salary_dep = 0
    sal_max_dept = 0
    n_employees_dept = 0
    for row in cur:
        cc +=1
        n_employees_dept += 1
        tot_salary_dep+=row[1]
        if row[1] > sal_max_dept:
            sal_max_dept = row[1] 
    avg_salary_dept = tot_salary_dep/n_employees_dept
    print('current employees with salary in ', d[key],' department are ',n_employees_dept,'\n   and the average salary per employee is ',avg_salary_dept,'\n   and the max salary in this department is: ',sal_max_dept)        
print('current employees wih salary: ',cc)

#What is the count of current employees who are aged 70 and above distributed by department
total_above_seventy = 0
for key in d:
    cur.execute('SELECT salaries.emp_no, salaries.to_date, employees.birth_date, dept_emp.dept_no FROM salaries JOIN employees,dept_emp ON salaries.emp_no = employees.emp_no AND salaries.emp_no = dept_emp.emp_no WHERE salaries.to_date = "9999-01-01" AND dept_no = "%s" AND birth_date < "1952-03-02"'%key)
    above_seventy = 0 
    for row in cur:
        above_seventy += 1
    print('above 70 in %s department: %d'%(d[key],above_seventy))
    total_above_seventy += above_seventy
print('total above seventy: ', total_above_seventy)

#What is the average salary for employees grouped by titles?
cur.execute('SELECT * FROM titles')
titles_list = []
for row in cur:
    if not row[1] in titles_list:
        titles_list.append(row[1])
print(titles_list)
pi = 0
for title in titles_list:
    cur.execute('SELECT salaries.emp_no, salaries.to_date, titles.to_date, titles.title, salaries.salary FROM salaries JOIN titles ON salaries.emp_no = titles.emp_no WHERE salaries.to_date = "9999-01-01" AND titles.to_date = "9999-01-01" AND titles.title = "%s"'%title)
    r = 0
    salary = 0
    for row in cur:
        r += 1
        pi += 1
        salary += row[4]
    averg_salary_title = salary/r
    print (title,r, salary/r)
print('pi: ',pi)

#What is the head count of current employees grouped first by department and then by titles?
cur.execute('DROP TABLE IF EXISTS report')
cur.execute('CREATE TABLE report(department TEXT, Senior_Engineer INTEGER, Staff INTEGER, Engineer INTEGER, Senior_Staff INTEGER, Assistant_Engineer INTEGER, Technique_Leader INTEGER, Manager INTEGER)')
tab = []
for keys in d:
    dep_title_list = []
    dep_title_list.append(d[keys])
    for titl in titles_list:
        count =0
        cur.execute('SELECT salaries.emp_no, salaries.to_date, titles.to_date, dept_emp.to_date, titles.title, dept_emp.dept_no FROM salaries JOIN titles,dept_emp ON salaries.emp_no = titles.emp_no AND salaries.emp_no = dept_emp.emp_no WHERE salaries.to_date = "9999-01-01" AND titles.to_date = "9999-01-01" AND dept_emp.to_date = "9999-01-01" AND titles.title = "%s" AND dept_no = "%s"'%(titl,keys))
        for row in cur:
            count +=1
        dep_title_list.append(count)
    dep_title_tuple = tuple(dep_title_list)
    tab.append(dep_title_tuple)
print(tab) 

for i in range(0,len(tab)):
    cur.execute('INSERT INTO report(department,Senior_Engineer,Staff,Engineer,Senior_Staff,Assistant_Engineer,Technique_Leader, Manager) VALUES (?,?,?,?,?,?,?,?)',tab[i])
conn.commit()

#cur.execute('SELECT salaries.emp_no, salaries.to_date, titles.to_date, titles.title FROM salaries JOIN titles,dept_emp ON salaries.emp_no = titles.emp_no AND salaries.emp_no = dept_emp.emp_no WHERE salaries.to_date = "9999-01-01" AND titles.to_date = "9999-01-01" AND titles.to_date = "9999-01-01" AND titles.title = "%s" AND dept_no = "%s"'%(element,key))
#Provide the answers in a short report