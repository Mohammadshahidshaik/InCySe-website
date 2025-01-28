document.getElementById("login").addEventListener("submit", function (e) {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  // Hardcoded credentials
  const credentials = [
    { username: "admin", password: "admin123" },
    { username: "employee", password: "employee123" }
  ];

  const validUser = credentials.find(
    (user) => user.username === username && user.password === password
  );

  if (validUser) {
    window.location.href = "../pages/employee.html"; // Redirect to a common dashboard
  } else {
    alert("Invalid username or password. Please try again!");
  }
});



document.getElementById("dashboardlogin").addEventListener("submit", function (e) {
  e.preventDefault();

  const password = document.getElementById("password").value;

  // Hardcoded credentials
  const credentials = [
    { password: "admin123" }
  ];

  const validUser = credentials.find(
    (user) => user.password === password
  );

  if (validUser) {
    window.location.href = "../pages/dashboard.html"; // Redirect to employee.html
  } else {
    alert("Invalid password. Please try again!");
  }
});
