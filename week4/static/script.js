document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("loginForm");
  const checkbox = document.getElementById("agree");

  form.addEventListener("submit", function (event) {
    if (!checkbox.checked) {
      event.preventDefault();
      alert("請勾選同意條款");
    }
  });

  const hotelForm = document.getElementById("hotelForm");
  hotelForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const id = document.getElementById("hotelId").value.trim();
    if (!/^[1-9]\d*$/.test(id)) {
      alert("請輸入正整數");
      return;
    }
    window.location.href = `/hotel/${id}`;
  });
});
