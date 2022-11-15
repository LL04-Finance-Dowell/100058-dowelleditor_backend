## How to use editor api -->

- To call the editor you need to follow all the steps below 
    1. Post data to editor api .
    2. url : `https://100058.pythonanywhere.com/dowelleditor/editor/`
    3. Data to be posted are :
    ```json
    {
        "database":"database_name",
        "collection":"collection_name",
        "fields": "fields_name",
        "document_id" : "document_id or a unique_id"
    }
    ```
    4. it will return a link , then you can redirect to that link.
- What is the process ?
    1. After you pot the required data to the url , it generate a link which is of editor .
    2. Editor app will use the provided data and call dowell targeted population function .
    3. According to the `document_id` it will fetch that particular document from the database and display in the editor .
- How to save ?
    1. if you wanna edit the document/article you can do and then you will have to click save button .
    2. After you click the save button it will save to a collection and return a `document_id` , using that you can fetch the data .
    3. In the document looks like :
    ```json
    {
        "_id":"objectId(document_id)",
        "eventId":"eventId",
        "raw_data":"actual data",
        "edited_data":"edited_data"
    }