/* Set font and background color */
body {
  font-family: Arial, sans-serif;
  background-color: #f3f3f3;
}

/* Center the form */
form {
  margin: 0 auto;
  max-width: 600px;
  padding: 20px;
  background-color: #ffffff;
  border: 1px solid #dddddd;
  box-shadow: 0px 1px 3px rgba(0,0,0,0.3);
}

/* Style the label and select elements */
label {
  display: block;
  margin-bottom: 10px;
  font-weight: bold;
}
select {
  display: block;
  margin-bottom: 20px;
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #cccccc;
  border-radius: 4px;
  box-sizing: border-box;
}

/* Style the submit button */
input[type="submit"] {
  background-color: #f0c14b;
  color: #111111;
  font-size: 16px;
  font-weight: bold;
  border: 1px solid #a88734;
  border-radius: 3px;
  padding: 10px 20px;
  cursor: pointer;
}

input[type="submit"]:hover {
  background-color: #ddb347;
  border: 1px solid #997029;
}

#header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #232f3e;
  color: #ffffff;
  padding: 10px 20px;
}

#logo {
  width: 150px;
  height: auto;
}

#title {
  font-size: 24px;
  font-weight: bold;
}

.nav-button {
  background-color: #232f3e;
  color: #ffffff;
  padding: 10px 20px;
  text-decoration: none;
  font-weight: bold;
  border-radius: 5px;
  transition: background-color 0.2s ease-in-out;
}

.nav-button:hover {
  background-color: #1a222e;
}