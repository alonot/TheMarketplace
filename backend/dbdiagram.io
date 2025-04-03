// Use DBML to define your database structure
// Docs: https://dbml.dbdiagram.io/docs

Table User {
  pk integer [primary key]
  email varchar
  username varchar [not null,unique]
  name varchar
  rollno varchar
  role varchar
  admin_id integer
  created_at timestamp [default: `now()`]
}

enum ParentType {
  PAYMENT
  ITEM
}

enum ANSWERFIELD {
  INTEGER
  IMG
  STRING
}

Table Question {
  id integer [primary key]
  question varchar [not null]
  payment_id integer [not null]
  field_type ANSWERFIELD
  field_len integer // can be null for image or infinite string
}

Table Answer {
  id integer [primary key]
  answer varchar [not null]
  question_id integer [not null]
  transaction_id integer [not null]
  image_answer integer // if the answer required is Image
}

Table Payment {
  id integer [primary key]
  user_id integer
  title varchar
  questions varchar
}

Table Image {
  id integer [primary key]
  data varbinary
  parent_id integer [not null]
  parent_type ParentType [not null]
}

Table Transaction {
  transaction_id integer [primary key]
  payment_method integer
  user_id integer
}

Table Item {
  id integer [primary key]
  title varchar
  approved_by integer [default: null]
  rejected_by integer [default: null]
}

Table Request {
  id integer [primary key]
  title varchar
  description varchar
  approved_by integer [default: null]
  rejected_by integer [default: null]
}

Table Tag {
  id varchar [primary key]
  name varchar [not null]
}


// Relationships
Ref User_payments: Payment.user_id > User.pk
Ref payment_question: Question.payment_id > Payment.id
Ref payment_answer: Answer.transaction_id > Transaction.transaction_id
Ref question_answer: Answer.question_id > Question.id
Ref answer_image: Answer.image_answer > Image.id
Ref Payment_images: Image.parent_id > Payment.id
Ref Item_images: Image.parent_id > Item.id 
Ref Transaction_user: Transaction.user_id > User.pk
Ref Item_approved_by: Item.approved_by > User.admin_id
Ref Item_rejected_by: Item.rejected_by > User.admin_id
Ref Request_approved_by: Request.approved_by > User.admin_id
Ref Request_rejected_by: Request.rejected_by > User.admin_id
Ref ItemTag_tag: Item.id <> Tag.id
Ref RequestTag_request: Request.id <> Tag.id
Ref transaction_payment : Transaction.payment_method > Payment.id

