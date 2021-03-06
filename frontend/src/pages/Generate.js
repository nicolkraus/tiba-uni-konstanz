import { React, Component } from "react";
import Introduction from "../components/Introduction";
import Transitions from "../components/Transitions";
import Interactions from "../components/Interactions";
import Plots from "../components/Plots";
import Infos from "../components/Infos";
import Upload from "../components/Upload";
import ExampleData from "../components/ExampleData";

export default class Generate extends Component {
  constructor() {
    super();
    this.state = {
      //upload
      upload: "",
      upload_successful: "",
      upload_response: "",
      //infos
      info_headers: "",
      info_ids: "",
      info_behaviors: "",
      info_categories: "",
      //interactions
      i_min_edge_count: 0,
      i_graph: null,
      //plot behavior time
      behavior: null,
      show_grid: true,
      p_image: null,
      options: ["one piece"],
      //transitions
      option: false,
      min_edge_count: 0,
      with_status: false,
      normalized: false,
      colored: false,
      colored_edge_thickness: 5,
      color_hue: 150,
      node_color_map: "total_time",
      node_size_map: "total_time",
      node_label_map: "total_time",
      graph: null,
    };
  }

  getTransitions = async () => {
    const formData = new FormData();
    formData.append("option", this.state["option"]);
    formData.append("min_edge_count", this.state["min_edge_count"]);
    formData.append("with_status", this.state["with_status"]);
    formData.append("normalized", this.state["normalized"]);
    formData.append("colored", this.state["colored"]);
    formData.append(
      "colored_edge_thickness",
      this.state["colored_edge_thickness"]
    );
    formData.append("color_hue", this.state["color_hue"]);
    formData.append("node_color_map", this.state["node_color_map"]);
    formData.append("node_size_map", this.state["node_size_map"]);
    formData.append("node_label_map", this.state["node_label_map"]);
    formData.append("upload", this.state["upload"]);

    await fetch("http://localhost:8000/api/transitions/", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => this.setState({ graph: data.graph }));
  };

  getInteractions = async () => {
    const formData = new FormData();
    formData.append("upload", this.state["upload"]);
    formData.append("min_edge_count", this.state["i_min_edge_count"]);

    await fetch("http://localhost:8000/api/interactions/", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => this.setState({ i_graph: data.graph }));
  };

  getBehaviorPlot = async () => {
    const formData = new FormData();
    formData.append("upload", this.state["upload"]);
    formData.append("behavior", this.state.behavior);

    await fetch("http://localhost:8000/api/behaviorplot/", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => this.setState({ p_image: data.plot }));
  };

  getInfo = async () => {
    const formData = new FormData();
    formData.append("upload", this.state["upload"]);

    await fetch("http://localhost:8000/api/infos/", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) =>
        this.setState({
          info_headers: data.headers,
          info_ids: data.ids,
          info_behaviors: data.behaviors,
          info_categories: data.categories,
          options: data.behaviors,
        })
      );
  };

  validateUpload = async () => {
    const formData = new FormData();
    formData.append("upload", this.state["upload"]);

    await fetch("http://localhost:8000/api/upload/", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) =>
        this.setState({
          upload_successful: data.success,
          upload_response: data.response,
        })
      );
  };

  updateExampleData = (obj) => {
    this.setState({ upload: obj[Object.keys(obj)[0]] }, () => {
      this.validateUpload();
      this.getInfo();
      this.getTransitions();
      this.getInteractions();
      this.getBehaviorPlot();
    });
  };

  updatePlot = (obj) => {
    this.setState({ [Object.keys(obj)[0]]: obj[Object.keys(obj)[0]] }, () => {
      this.getBehaviorPlot();
    });
  };

  updateInteractionNetwork = (obj) => {
    this.setState({ i_min_edge_count: obj[Object.keys(obj)[0]] }, () => {
      this.getInteractions();
    });
  };

  updateTransitionNetwork = (obj) => {
    this.setState({ [Object.keys(obj)[0]]: obj[Object.keys(obj)[0]] }, () => {
      this.getTransitions();
    });
  };

  updateUpload = (obj) => {
    this.setState({ [Object.keys(obj)[0]]: obj[Object.keys(obj)[0]] }, () => {
      this.validateUpload();
      this.getInfo();
      this.getTransitions();
      this.getInteractions();
      this.getBehaviorPlot();
    });
  };

  render() {
    return (
      <div>
        <Introduction />
        <Upload passUpload={this.updateUpload} />
        <ExampleData passExample={this.updateExampleData} />
        {this.state.upload_response && (
          <div className="padded">
            <h4>Unfortunately we cannot handle the provided data:</h4>
            <h5>{this.state.upload_response}</h5>
          </div>
        )}
        {this.state.upload_successful && (
          <Infos
            info_headers={this.state.info_headers}
            info_ids={this.state.info_ids}
            info_behaviors={this.state.info_behaviors}
            info_categories={this.state.info_categories}
          />
        )}
        {this.state.upload_successful && (
          <Interactions
            passValues={this.updateInteractionNetwork}
            graph={this.state.i_graph}
          />
        )}
        {this.state.upload_successful && (
          <Plots
            passValues={this.updatePlot}
            options={this.state.options}
            image={this.state.p_image}
          />
        )}
        {this.state.upload_successful && (
          <Transitions
            passValues={this.updateTransitionNetwork}
            graph={this.state.graph}
            normalized={this.state.normalized}
            colored={this.state.colored}
            with_status={this.state.with_status}
          />
        )}
      </div>
    );
  }
}
