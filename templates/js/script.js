// need to figure out how to link to html
            let cart = [];
            let data = [];

            function addItem() {
                const bookName = document.getElementById("book-title");
                localStorage.setItem("book", bookName.innerHTML);
                cart.push(bookName.innerHTML);
                return cart
            }

            function togglePopup() {
                document.getElementById("popup-1").classList.toggle("active");
            }

            function clicked() {
                data.append(addItem());
                let list = document.getElementById("added-book");
                data.forEach((item) => {
                    let li = document.createElement("li");
                    li.innerText = item;
                    list.appendChild(li);
                });
            }

            var csvFileData = cart

            function download_csv_file() {
                var csv = 'To Be Read:\n';
                csvFileData.forEach(function (row) {
                    csv += row;
                    csv += "\n";
                });
                var hiddenElement = document.createElement('a');
                hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
                hiddenElement.target = '_blank';
                hiddenElement.download = 'to_be_read.csv';
                hiddenElement.click();
            }

            document.getElementById("added-book").innerHTML = localStorage.getItem("book");
