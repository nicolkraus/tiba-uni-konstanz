import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import "../css/layout.css";

export default function ExampleData(props) {
  const header = `#### Alternative: Load Example Data
	`;
  const description = `
* **Benefactor**: Etienne Lein, Max Planck Institute of Animal Behavior
* **Description**: [Lein](https://www.ab.mpg.de/person/98178) studies the evolution of social behavior in the Lamprologine cichlids of Lake Tanganyika. Therefore, he films underwater and derives datasets by logging events with [BORIS](https://www.boris.unito.it). Each of the following examples shows the behavioral events of one species derived from 20-minute videos.
	`;
  const loadExample = (e) => {
    props.passExample({
      [e.target.name]: e.target.name,
    });
  };

  return (
    <div className="padded text">
      <ReactMarkdown children={header} remarkPlugins={[remarkGfm]} />
      <div className="border background ">
        <ReactMarkdown children={description} remarkPlugins={[remarkGfm]} />
        <button name="example1" className="button" onClick={loadExample}>
          Example 1: Neolamprologus multifasciatus
        </button>
        <p> </p>
        <button name="example2" className="button" onClick={loadExample}>
          Example 2: Telmatochromis temporalis (dwarf morph)
        </button>
        <p> </p>
        <button name="example3" className="button" onClick={loadExample}>
          Example 3: Lamprologus ocellatus
        </button>
      </div>
    </div>
  );
}
