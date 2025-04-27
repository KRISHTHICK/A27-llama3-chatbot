1. Comment: Instead of hardcoding `"sample.txt"`, allow the user to upload a file via Streamlit’s `file_uploader` for more flexibility.  
2. Comment: Create the vector store outside the app run or cache it to avoid recomputing embeddings every time the app reloads (`@st.cache_resource`).  
3. Comment: Loading documents and splitting should be modularized into separate functions for better readability and future maintenance.  
4. Comment: Add basic exception handling around loading documents and running inference to prevent the app from crashing on errors.  
5. Comment: `import os` is unused—safe to remove to clean up imports.  

---

I reviewed the code and left suggestions to improve coding quality. ✅
