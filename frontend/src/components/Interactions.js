import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "../css/images.css";

export default function Interactions(props) {
  const header = `#### Interaction network
`;
  const description = `
Displays interactions in form of a directed weighted graph. Nodes represent the individuals in the dataset. An edge is drawn from *A* to *B* if a row in the dataset has *A* as the *Subject* and *B* as *Modifier 1*. The edge weigth represents the amount of such rows. **Requires optional column**: *Modifier 1*
`;
  const handleChange = (e) => {
    props.passValues({
      [e.target.name]: e.target.value ? e.target.value : 0,
    });
  };

  return (
    <div className="padded text">
      <ReactMarkdown children={header} remarkPlugins={[remarkGfm]} />
      <div className="border background">
        <ReactMarkdown children={description} remarkPlugins={[remarkGfm]} />
        <br></br>
        <label htmlFor="min_edge_count">
          <b>Remove edges</b> with edge weights below
        </label>
        <input
          className="params"
          name="min_edge_count"
          type="number"
          id="min_edge_count"
          min="0"
          onChange={handleChange}
        ></input>
        <div className="imgbox">
          <img className="center-fit" src={props.graph} alt="loading ..." />
        </div>
      </div>
    </div>
  );
}
