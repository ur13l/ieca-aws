fetch("https://gswtel7x7e.execute-api.us-east-2.amazonaws.com/prod/instances", {
  headers: {
    "Content-Type": "application/json",
    "x-api-key": "OC1vBuuIkiiLvaLZGi2J4Mnb51wntEo8N3AObv45",
  },
})
  .then((response) => response.json())
  .then((data) => {
    const list = document.getElementById("list");
    data.body.forEach((instance) => {
      const li = document.createElement("li");
      li.innerText =
        instance.InstanceId + " - " + instance.State + " - " + instance.Name;
      list.appendChild(li);
    });
  });
