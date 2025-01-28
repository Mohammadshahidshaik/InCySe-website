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
  