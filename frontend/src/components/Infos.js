import React from "react";
import { Table } from "react-bootstrap";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function DisplayInfos(props) {
  /**
   * Displays a table with information on the selected dataset.
   * The information consists of Subjects, Behaviors and Behavioral Categories
   */

  const title = "#### General Information";

  //cut garbage at array borders
  const ids = JSON.stringify(props.info_ids).slice(1, -1);
  const behaviors = JSON.stringify(props.info_behaviors).slice(1, -1);
  const categories = JSON.stringify(props.info_categories).slice(1, -1);

  //return title and table
  return (
    <div className="padded text ">
      <ReactMarkdown children={title} remarkPlugins={[remarkGfm]} />
      <div className="border background">
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>Identified column</th>
              <th>Values</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Subject</td>
              <td>{ids}</td>
            </tr>
            <tr>
              <td>Behavior</td>
              <td>{behaviors}</td>
            </tr>
            <tr>
              <td>Behavioral Category</td>
              <td>{categories}</td>
            </tr>
          </tbody>
        </Table>
      </div>
    </div>
  );
}
