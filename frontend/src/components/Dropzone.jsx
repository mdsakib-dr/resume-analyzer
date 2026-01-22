
// import React from "react";
// import { useDropzone } from "react-dropzone";

// export default function Dropzone({ file, setFile }) {
//   const { getRootProps, getInputProps, isDragActive } = useDropzone({
//     accept: { "application/pdf": [] },
//     onDrop: (files) => setFile(files[0])
//   });

//   return (
//     <div className="dropzone-wrapper">
//       <div {...getRootProps()} className="dropzone">
//         <input {...getInputProps()} />
//         {isDragActive ? (
//           <p>Drop the resume PDF here...</p>
//         ) : (
//           <p>Drag & drop resume PDF here, or click to upload</p>
//         )}
//       </div>

//       {/* ✅ SHOW UPLOADED FILE */}
//       {file && (
//         <div className="file-info">
//           <p>
//             <b>Uploaded file:</b> {file.name} (
//             {(file.size / 1024).toFixed(1)} KB)
//           </p>
//         </div>
//       )}
//     </div>
//   );
// }
import React from "react";
import { useDropzone } from "react-dropzone";

export default function Dropzone({ file, setFile, clearResult }) {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: { "application/pdf": [] },
    onDrop: (files) => {
      setFile(files[0]);
      clearResult(); // ✅ clear old result when new file uploaded
    }
  });

  // const removeFile = () => {
  //   setFile(null);
  //   clearResult();
  // };

  return (
    <div className="dropzone-wrapper">
      <div {...getRootProps()} className="dropzone">
        <input {...getInputProps()} />
        {isDragActive ? (
          <p>Drop the resume PDF here...</p>
        ) : (
          <p>Drag & drop resume PDF here, or click to upload</p>
        )}
      </div>

      {file && (
        <div className="file-info">
          <p>
            <b>Uploaded:</b> {file.name} (
            {(file.size / 1024).toFixed(1)} KB)
          </p>

          
        </div>
      )}
    </div>
  );
}
