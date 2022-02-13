var fileInput = document.getElementById("file"),

    readFile = function () {
        var reader = new FileReader();
        reader.onload = function () {
            console.log(reader.result);
        };
        // start reading the file. When it is done, calls the onload event defined above.
        reader.readAsBinaryString(fileInput.files[0]);
    };

fileInput.addEventListener('change', readFile);