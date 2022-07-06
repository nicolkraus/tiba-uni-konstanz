import React, { useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function Plot(props) {
  const header = `#### Behavior inspection 
  `;
  const description = ` 
Displays a plot with *Time* on the x-axis and the amount of behavioral events (accumulated) on the y-axis. Each colored line represent one individual. A dashed line indicates the time before the first and after the last occurence of the specified behavior.`;

  useEffect(
    () => props.passValues({ behavior: props.options[0] }),
    [props.options]
  );

  const change = (e) => {
    props.passValues({ [e.target.name]: e.target.value });
  };

  return (
    <div className="padded text">
      <ReactMarkdown children={header} remarkPlugins={[remarkGfm]} />
      <div className="border background">
        <ReactMarkdown children={description} remarkPlugins={[remarkGfm]} />
        <br></br>
        <label htmlFor="behavior">
          Choose <b>behavior</b> to display
        </label>
        <select
          className="params"
          name="behavior"
          id="behavior"
          onChange={change}
        >
          {props.options.map((item) => {
            return (
              <option key={item} value={item}>
                {item}
              </option>
            );
          })}
        </select>
        <p> </p>
        <div className="imgbox">
          <img className="center-fit" src={props.image} alt="not loaded" />
        </div>
      </div>
    </div>
  );
}
