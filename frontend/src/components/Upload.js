import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import "../css/layout.css";

export default function Upload(props) {
  /**
   * Enables the user to upload a file
   */

  const title = "#### File Upload";
  const description = `
* **Accepted filetypes**: *.xlsx*, *.csv*
* **Required columns**: *Time*, *Subject*, *Behavior*
* **Optional columns**: *Modifier 1*, *Behavioral category*
`;

  //pass input to parent component
  const handleFileChange = (e) => {
    props.passUpload({
      [e.target.name]: e.target.files[0],
    });
  };

  //return the title followed by description and file input widget
  return (
    <div className="padded text">
      <ReactMarkdown children={title} remarkPlugins={[remarkGfm]} />
      <div className="border background">
        <ReactMarkdown children={description} remarkPlugins={[remarkGfm]} />
        <input
          type="file"
          name="upload"
          accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
          onChange={handleFileChange}
        ></input>
      </div>
    </div>
  );
}
