function searchPhotos() {
    const query = document.getElementById('searchQuery').value.trim();
    const resultDiv = document.getElementById('searchResults');

    if (!query) {
        resultDiv.innerHTML = 'Please enter a search term.';
        return;
    }

    resultDiv.innerHTML = '';  
    
    const apigClient = apigClientFactory.newClient({
        apiKey: ""
});

    const params = {
        q: query  
    };

    apigClient.searchGet(params, {}, {})
        .then(function(response) {
            console.log(response);
            console.log(response.data.imagePaths);
            const photos = response.data.imagePaths;
            if (photos.length > 0) {
                photos.forEach(photo => {
                    const imgElement = document.createElement('img');
                    imgElement.src = photo;
                    imgElement.style.width = '100px';
                    resultDiv.appendChild(imgElement);
                });
            } else {
                resultDiv.innerHTML = 'No photos found.';
            }
        }).catch(function(error) {
            console.error('Search failed:', error);
            resultDiv.innerHTML = 'Search failed. See console for details.';
        });
}

function uploadPhoto() {
    const photoInput = document.getElementById('photoUpload');
    const labelInput = document.getElementById('customLabels');

    const photoFile = photoInput.files[0];
    const customLabels = labelInput.value;

    const headers = {
        'Content-Type': 'image/*',
        'x-amz-meta-customLabels': customLabels,
        'x-api-key': ''
    };
    let config = {headers: headers}

    url = "//API Gateway Endpoint" + photoFile.name
    console.log(photoFile.name)

    axios.put(url,photoFile,config).then(response => {
        console.log(response.data);
        alert("Upload successful!");
        photoInput.value = '';
        labelInput.value = '';
    })
    .catch(error => {
        console.error("Upload failed:", error);
        alert("Upload failed. Please try again.");
      });
}