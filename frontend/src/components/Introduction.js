import React from "react";
import { Table } from "react-bootstrap";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function Introduction() {
  /**
   * Gives a general description of the website.
   * Displays a data template to download.
   */

  const title = "#### Introduction";
  const description = `
* **What is this tool?**: T.I.B.A. allows behavioral data to be uploaded and analyzed. For this purpose, various networks and diagrams are generated, which may be parameterized by the user. The target audience are behavioral bioligists, yet the tool may be used by anyone with appropiate data wanting to inspect it or derive networks and diagrams.
* **How to start?**: If you have data with the required columns as specified below, just click the File Upload button, everything will be computed automatically with default values. If you do not have data, just load one of the example datasets by clicking on it.
* **Required data format: Below is a template with all required and optional columns. Some values are filled so you get a feeling how to populate your own. Also, you may download an empty template.
        `;

  return (
    <div className="padded text">
      <ReactMarkdown children={title} remarkPlugins={[remarkGfm]} />
      <div className="border background">
        <ReactMarkdown children={description} remarkPlugins={[remarkGfm]} />
      </div>
      <div className="border background">
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>Time</th>
              <th>Subject</th>
              <th>Behavior</th>
              <th>Behavioral category</th>
              <th>Modifier 1</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>0.00</td>
            </tr>
            <tr>
              <td>monkey_1</td>
            </tr>
            <tr>
              <td>jumping </td>
            </tr>
            <tr>
              <td>movement</td>
            </tr>
            <tr>
              <td></td>
            </tr>
            <tr>
              <td>START</td>
            </tr>
          </tbody>
        </Table>
      </div>
    </div>
  );
}
