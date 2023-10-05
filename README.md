# Project Task for September

Create a system for uploading and sharing documents. The system will consist of three roles: student, professor, and administrator.

#### Professor Role:

* Authentication
* Document creation
* Document sharing
* Document deletion
* Revoke document sharing
* View created documents (sorted by creation date)

#### Student Role:

* Authentication
* View a list of documents shared with the student, sorted by the date they were created
* Sort documents by the following criteria:
* Alphabetically by name
* By creation date
* Filter documents by the professor's name (professors' names can be in a dropdown)

#### Administrator Role:

* Authentication
* Create users (students and professors)
* Option to edit and delete users
* View all users sorted by the student/professor criterion

#### Database Structure:

* Users table (expand the AbstractUser class with a user role attribute or add a new table to define roles)
Documents table - attributes are id (primary key), document title (varchar), path to the document saved on the server (varchar), document creation time, creator (foreign key - which professor created the document)
* Student_document (intermediate table) to define which students the document is shared with - attributes are id (primary key), document (foreign key to the Document model), student (foreign key to the User model with the Student role). Optionally, a combined key of two foreign keys can be used instead of a primary key.
* Admin has pages for CRUD (Create, Read, Update, Delete) users. Users are sorted by role.
* Professor has page(s) for CRUD their documents. Professors also have page(s) for sharing uploaded documents with students. * Professors should be able to revoke sharing that they previously did with a specific student. Professors should be able to share a document with multiple students in one action (not one student at a time). The document view is sorted by creation date.
* Students have a page with a list of documents shared with them. Students should be able to access shared documents. The student can sort the list of documents by creation date or document name. Students can also filter the list by professor.

To store documents, use a File Storage System, and save the path to the saved document in the database. All changes in the database should be made via POST requests. When deleting a document, take care of physically deleting the document from the storage location in addition to removing the path from the database.

Pay attention to the security of the application (password encryption, etc.). The application will have a login and logout page accessible to all users. Code should be developed using the Django framework. Organize and implement the code according to the MVC (MVT) architecture. It is mandatory to have a structure that can be relatively easily expanded with minor additional functionalities. Functionality and security are the main aspects, but usability of the interface and code organization will also be considered in the evalua
