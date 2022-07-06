import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "../css/images.css";

export default function Transitions(props) {
  const header = `#### Transition network`;
  const description = ` 
Displays behavioral transitions in form of a directed, weighted graph. Nodes represent behaviors, edges represent the transition from one behavior to another. The total amount of transitions or the transition probabilites, i.e. the probability of animals showing the behavior at which the edge is incoming after the behavior from which the edge is outgoing, may be used as edge weighting. `;
  const list = `
* **Full functionality only with optional columns**: *Status*, *Behavioral category*
* **Parameters**:
    - **Colored edge thickness** - Set edge thickness of individual colored edges.
  - **Minimal edge weight** - Removes all edges below specified value.
  - **Mappings** - Map *total time*, *average time* or *amount* of behaviors to their respective node size, label or color density.
    - **Color hue** - Set the color hue for the *node color mapping*
`;

  const handleChange = (e) => {
    props.passValues({
      [e.target.name]: e.target.value,
    });
  };

  const changeWithDefault = (e) => {
    if (props.normalized && e.target.value > 0.99) {
      props.passValues({
        [e.target.name]: 0,
      });
    } else {
      props.passValues({
        [e.target.name]: e.target.value ? e.target.value : 0,
      });
    }
  };

  const handleCheckboxChange = (e) => {
    props.passValues({
      [e.target.name]: e.target.checked,
    });
  };

  return (
    <div className="padded">
      <div className="text">
        <ReactMarkdown children={header} remarkPlugins={[remarkGfm]} />
        <div className="border background">
          <ReactMarkdown children={description} remarkPlugins={[remarkGfm]} />
          <br></br>
          <hr className="hr"></hr>
          {/*checkbox categories as nodes*/}
          <div className="form-check mb-2 mr-sm-2">
            <input
              type="checkbox"
              className="form-check-input"
              name="option"
              id="option"
              onChange={handleCheckboxChange}
            ></input>
            <label className="form-check-label" htmlFor="normalized">
              <b>Behavioral Categories:</b>&nbsp; Set behavioral categories
              instead of behaviors as nodes
            </label>
          </div>
          {/*checkbox normalized*/}
          <div className="form-check mb-2 mr-sm-2">
            <input
              type="checkbox"
              className="form-check-input"
              name="normalized"
              id="normalized"
              onChange={handleCheckboxChange}
            ></input>
            <label className="form-check-label" htmlFor="normalized">
              <b>Transition probabilities:</b>&nbsp; Set transition probabilites
              as edge weights (logarithmically normalized)
            </label>
          </div>
          {/*checkbox with status*/}
          <div className="form-check mb-2 mr-sm-2">
            <label className="form-check-label" htmlFor="colored">
              <b>Behavior status:</b>&nbsp; Create separate nodes for starting
              and stopping behaviors
            </label>
            <input
              type="checkbox"
              className="form-check-input"
              name="with_status"
              id="with_status"
              onChange={handleCheckboxChange}
            ></input>
          </div>
          {/*checkbox colored*/}
          <div className="form-check mb-2 mr-sm-2">
            <label className="form-check-label" htmlFor="colored">
              <b>Unique colored graph:</b>&nbsp; A unique color for each node
              and its outgoing edges
            </label>
            <input
              type="checkbox"
              className="form-check-input"
              name="colored"
              id="colored"
              onChange={handleCheckboxChange}
            ></input>
          </div>
          {/* colored edge thickness */}
          {props.colored && (
            <div className="params">
              <div className="custom-slider">
                <label
                  htmlFor="colored_edge_thickness"
                  className="form-check-label"
                >
                  Colored edge thickness:
                </label>
                <input
                  name="colored_edge_thickness"
                  id="colored_edge_thickness"
                  type="range"
                  min="1"
                  max="15"
                  onChange={handleChange}
                ></input>
              </div>
            </div>
          )}
          <hr className="hr"></hr>
          {/*node size mapping*/}
          <div className="mappings">
            <label className="form-check-label" htmlFor="node_size_map">
              Map <b>node size</b>&nbsp;to
            </label>
            <select
              className="params"
              name="node_size_map"
              id="node_size_map"
              onChange={handleChange}
            >
              <option key="2" value="total_time">
                Total time
              </option>
              <option key="3" value="avg_time">
                Average time
              </option>
              <option key="4" value="amount">
                Number of occurences
              </option>
            </select>
          </div>
          {/*node label mapping*/}
          <div className="mappings">
            <label className="form-check-label" htmlFor="node_label_map">
              Map <b>node label</b>&nbsp;to
            </label>
            <select
              className="params"
              name="node_label_map"
              id="node_label_map"
              onChange={handleChange}
            >
              <option key="1" value="">
                -
              </option>
              <option key="2" value="total_time">
                Total time
              </option>
              <option key="3" value="avg_time">
                Average time
              </option>
              <option key="4" value="amount">
                Number of occurences
              </option>
            </select>
          </div>
          {/*node color mapping*/}
          {!props.with_status && !props.colored && (
            <div className="mappings">
              <label className="form-check-label" htmlFor="node_color_map">
                Map <b>node color</b>&nbsp;to
              </label>
              <select
                className="params"
                name="node_color_map"
                id="node_color_map"
                onChange={handleChange}
              >
                <option key="2" value="total_time">
                  Total time
                </option>
                <option key="3" value="avg_time">
                  Average time
                </option>
                <option key="4" value="amount">
                  Number of occurences
                </option>
              </select>
            </div>
          )}
          {/*color hue */}
          {!props.with_status && !props.colored && (
            <div className="params custom-slider">
              <label htmlFor="color_hue" className="form-check-label">
                Choose <b>color hue</b>
              </label>
              <input
                name="color_hue"
                id="color_hue"
                type="range"
                min="0"
                max="180"
                onChange={handleChange}
              ></input>
            </div>
          )}
          {/*number input for minimal edge weight*/}
          <div className="params custom-slider">
            <label htmlFor="min_edge" className="form-check-label">
              <b>Remove edges</b> with edge weights below
            </label>
            {props.normalized && (
              <input
                name="min_edge_count"
                id="min_edge"
                type="number"
                min="0"
                max="1"
                step="0.01"
                onChange={changeWithDefault}
              ></input>
            )}
            {!props.normalized && (
              <input
                name="min_edge_count"
                id="min_edge"
                type="number"
                min="1"
                onChange={changeWithDefault}
              ></input>
            )}
          </div>
          {/*image display*/}
        </div>
      </div>
      <div className="imgbox">
        <img className="center-fit" src={props.graph} alt="loading ..." />
      </div>
    </div>
  );
}
