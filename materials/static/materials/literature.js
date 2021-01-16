class MaterialRow extends React.Component {
    render() {
      return (
        <tr style={this.props.style}>
            <td>{this.props.row.title}</td>
            <td></td>
            <td>{this.props.row.pdf ? <a href={this.props.row.pdf}><i className="fas fa fa-download"></i></a> :
            (this.props.row.djvu ? <a href={this.props.row.djvu}><i className="fas fa fa-download"></i></a> : null)}
            </td>
        </tr>
      );
    }
  }
  
  class MaterialTable extends React.Component {
    render() {
      return (
        <table className="table table-striped mb-4">
          <tbody id="LiteratureTable">
            {this.props.rows}
          </tbody>
        </table>
      );
    }
  }

  class Literature extends React.Component {
    render() {
      const rows = [];
      const style = {borderLeft: "4px solid lightgray"}
      this.props.literature.forEach(row => {
        rows.push(
          <MaterialRow row={row} key={row.id} style={style} />
        );
      });
      return(
        <div>
          <MaterialTable rows={rows} />
        </div>
      );
    }

  }

  class ContentHeaders extends React.Component {
    render() {
      const options = [];
      const supersections = ["Механіка"];
      supersections.forEach(element => {
        options.push(
          <option value={element.title}>{element.title}</option>
        );
      });
      return (
          <div className="row justify-content-between">
              <div className="col-3 form-inline d-flex justify-content-center md-form form-sm my-0">
                  <i className="fas fa-search" aria-hidden="true"></i>
                  <input className="form-control form-control-sm ml-3 w-75" id="LiteratureSearch" type="text" placeholder="Назва/Автор">
                  </input>
              </div>
              <div className="col-3 mr-0">
                  <select className="selectpicker pb-2" multiple title="Розділи" data-style="z-depth-0 border-bottom black-text" data-dropdown-align-right="true">
                     {options}
                  </select>
              </div>
          </div>
      );
    }
  }


  class Content extends React.Component {
    render() {
      return (
        <div className="col-md-12 col-xl-8">
          <ContentHeaders type={this.props.type} />
          <Literature literature={this.props.literature} type={this.props.type} />
        </div>
      );
    }
  }

const material_content = document.getElementById('material-content');
const type = material_content.dataset.type;

fetch(`/literature_api/${type}`)
.then (response => response.json())
.then (literature => {
    ReactDOM.render(<Content literature={literature} type={type} />, document.getElementById('material-content'));
});