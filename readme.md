To run Application
python3 restaurant_app.py

Main.py 
 - Here we can change the database name
 - Host , port & debug

package.py 
  All the libraries are imported here , it helps to minimize the work, later this file is imported in rest files (import libraries only which is common to all the files)

Session 
  Here I have used Flask session , we can also Flask-Login as well

Input/Output -> Json format 
Could have used form also ( helps when we have to upload image as well) 
Could have added error status code for False return

billing is missed - new table named billing_details( order number , order date , order time , waiter , total_bill , price)

Features
 - Which table is most used ( table not used may have some defect)
 - We can take customer details  - loyal customer can be given discounts 
 - Peak Hours - Waiters / chefs add/remove
 - Inventory management
 - Waiter ratings ( if waiter gets more negative rating can be removed)

