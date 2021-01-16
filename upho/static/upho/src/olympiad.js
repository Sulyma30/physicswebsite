var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var TourOptions = function (_React$Component) {
  _inherits(TourOptions, _React$Component);

  function TourOptions(props) {
    _classCallCheck(this, TourOptions);

    var _this = _possibleConstructorReturn(this, (TourOptions.__proto__ || Object.getPrototypeOf(TourOptions)).call(this, props));

    _this.handleChangeTour = _this.handleChangeTour.bind(_this);
    return _this;
  }

  _createClass(TourOptions, [{
    key: "handleChangeTour",
    value: function handleChangeTour(tour, e) {
      this.props.handleChangeTour(tour);
    }
  }, {
    key: "render",
    value: function render() {
      var _this2 = this;

      var options = [];
      this.props.tour_options.forEach(function (tour) {
        options.push(React.createElement(
          "li",
          { key: tour, className: "nav-item" },
          React.createElement(
            "a",
            { className: "nav-link " + (_this2.props.tour === tour ? "active show " : ""), onClick: function onClick(e) {
                return _this2.handleChangeTour(tour, e);
              }, "data-toggle": "tab", role: "tab", "aria-controls": tour, "aria-selected": _this2.props.tour == tour ? "true" : "false" },
            tour.substring(0, 4),
            React.createElement(
              "span",
              { className: "d-none d-md-inline-block" },
              tour.substring(4)
            )
          )
        ));
      });
      return React.createElement(
        "div",
        { className: "mx-2" },
        React.createElement(
          "ul",
          { className: "nav justify-content-center", id: "TourTab", role: "tablist" },
          options
        )
      );
    }
  }]);

  return TourOptions;
}(React.Component);

var GradeOptions = function (_React$Component2) {
  _inherits(GradeOptions, _React$Component2);

  function GradeOptions(props) {
    _classCallCheck(this, GradeOptions);

    var _this3 = _possibleConstructorReturn(this, (GradeOptions.__proto__ || Object.getPrototypeOf(GradeOptions)).call(this, props));

    _this3.handleChangeGrade = _this3.handleChangeGrade.bind(_this3);
    return _this3;
  }

  _createClass(GradeOptions, [{
    key: "handleChangeGrade",
    value: function handleChangeGrade(e) {
      this.props.handleChangeGrade(e);
    }
  }, {
    key: "componentDidUpdate",
    value: function componentDidUpdate() {
      $('.selectpicker').selectpicker('refresh');
    }
  }, {
    key: "componentDidMount",
    value: function componentDidMount() {
      $('.selectpicker').selectpicker('refresh');
    }
  }, {
    key: "render",
    value: function render() {
      var _this4 = this;

      var options = [];
      this.props.grade_options.forEach(function (grade) {
        options.push(
        // Check whether it is 8-11 grades
        grade != 0 ? React.createElement(
          "option",
          { value: grade, key: grade },
          grade,
          " \u043A\u043B\u0430\u0441"
        ) : React.createElement(
          "option",
          { value: grade, key: grade },
          "\u0412\u0441\u0456 \u043A\u043B\u0430\u0441\u0438"
        ));
      });
      return React.createElement(
        "select",
        { className: "selectpicker", "data-style": "btn-bg olymp-files-select z-depth-0 px-1", "data-width": "130px", onChange: function onChange(e) {
            return _this4.handleChangeGrade(e);
          } },
        options
      );
    }
  }]);

  return GradeOptions;
}(React.Component);

var YearOptions = function (_React$Component3) {
  _inherits(YearOptions, _React$Component3);

  function YearOptions(props) {
    _classCallCheck(this, YearOptions);

    var _this5 = _possibleConstructorReturn(this, (YearOptions.__proto__ || Object.getPrototypeOf(YearOptions)).call(this, props));

    _this5.handleChangeEvent = _this5.handleChangeEvent.bind(_this5);
    return _this5;
  }

  _createClass(YearOptions, [{
    key: "handleChangeEvent",
    value: function handleChangeEvent(e) {
      this.props.handleChangeEvent(e);
    }
  }, {
    key: "componentDidUpdate",
    value: function componentDidUpdate() {
      $('.selectpicker').selectpicker('refresh');
    }
  }, {
    key: "componentDidMount",
    value: function componentDidMount() {
      $('.selectpicker').selectpicker('refresh');
    }
  }, {
    key: "render",
    value: function render() {
      var _this6 = this;

      var options = [];
      var i = 0;
      this.props.events.forEach(function (event) {
        var subtext = _this6.props.type == 'national' ? event.location : "";
        options.push(React.createElement(
          "option",
          { value: i, key: event.year, "data-subtext": subtext },
          event.year,
          " \u0440\u0456\u043A"
        ));
        i++;
      });
      return React.createElement(
        "select",
        { className: "selectpicker", "data-style": "btn-bg olymp-files-select z-depth-0 pl-2", "data-width": "140px", "data-show-subtext": "false", "data-live-search": "true", "data-size": "5", value: this.props.year, onChange: function onChange(e) {
            return _this6.handleChangeEvent(e);
          } },
        options
      );
    }
  }]);

  return YearOptions;
}(React.Component);

var DownloadButton = function (_React$Component4) {
  _inherits(DownloadButton, _React$Component4);

  function DownloadButton() {
    _classCallCheck(this, DownloadButton);

    return _possibleConstructorReturn(this, (DownloadButton.__proto__ || Object.getPrototypeOf(DownloadButton)).apply(this, arguments));
  }

  _createClass(DownloadButton, [{
    key: "render",
    value: function render() {
      var active_text = "Умови";
      var disabled_text = "Умов немає";
      if (this.props.solutions === true) {
        active_text = "Розв'язки";
        disabled_text = "Розв'язків немає";
      }
      var btn_disabled = React.createElement(
        "button",
        { className: "btn-md btn-white waves-effect px-1 py-4 olymp-files-btn z-depth-1 disabled" },
        disabled_text
      );
      var btn_active = React.createElement(
        "a",
        { href: this.props.link, target: "_blank", className: "btn-lg btn-white waves-effect px-2 py-4 px-sm-3 olymp-files-btn z-depth-1" },
        active_text,
        React.createElement("i", { className: "fas fa fa-file-download" })
      );
      return React.createElement(
        "div",
        { className: "d-flex justify-content-center px-1 col my-1" },
        this.props.link === "" ? btn_disabled : btn_active
      );
    }
  }]);

  return DownloadButton;
}(React.Component);

var OlympSelector = function (_React$Component5) {
  _inherits(OlympSelector, _React$Component5);

  function OlympSelector(props) {
    _classCallCheck(this, OlympSelector);

    var _this8 = _possibleConstructorReturn(this, (OlympSelector.__proto__ || Object.getPrototypeOf(OlympSelector)).call(this, props));

    _this8.state = {
      event: _this8.props.events[0],
      tour: _this8.props.events[0].files[0].tour,
      grade: _this8.props.events[0].files[0].grade
    };
    _this8.handleChangeEvent = _this8.handleChangeEvent.bind(_this8);
    _this8.handleChangeTour = _this8.handleChangeTour.bind(_this8);
    _this8.handleChangeGrade = _this8.handleChangeGrade.bind(_this8);
    return _this8;
  }

  _createClass(OlympSelector, [{
    key: "handleChangeEvent",
    value: function handleChangeEvent(event) {
      this.setState({ event: this.props.events[event.target.value] });
    }
  }, {
    key: "handleChangeTour",
    value: function handleChangeTour(tour) {
      this.setState({ tour: tour });
    }
  }, {
    key: "handleChangeGrade",
    value: function handleChangeGrade(event) {
      this.setState({ grade: parseInt(event.target.value) });
    }
  }, {
    key: "render",
    value: function render() {
      var _this9 = this;

      // Get links for files if they exist
      var links = {
        'problems': "",
        'solutions': ""
      };
      this.state.event.files.map(function (file) {
        if (file.tour === _this9.state.tour && file.grade === _this9.state.grade) {
          links['problems'] = file.problems === null ? "" : file.problems;
          links['solutions'] = file.solutions === null ? "" : file.solutions;
        }
      });
      return React.createElement(
        "div",
        { className: "pt-4" },
        React.createElement(TourOptions, { tour: this.state.tour, tour_options: this.props.tour_options, handleChangeTour: this.handleChangeTour }),
        React.createElement(
          "div",
          { id: "olymp-files-selectors", className: "row row-cols-2 row-cols-md-4 mx-1 px-1 py-3 justify-content-center z-depth-5" },
          React.createElement(
            "div",
            { className: "col py-2", id: "year-options" },
            React.createElement(YearOptions, { type: this.props.type, events: this.props.events, tour: this.state.tour, year: this.state.year, handleChangeEvent: this.handleChangeEvent })
          ),
          React.createElement(
            "div",
            { className: "col border-left py-2" },
            React.createElement(GradeOptions, { grade_options: this.props.grade_options, grade: this.state.grade, handleChangeGrade: this.handleChangeGrade })
          ),
          React.createElement(DownloadButton, { solutions: false, link: links.problems }),
          React.createElement(DownloadButton, { solutions: true, link: links.solutions })
        )
      );
    }
  }]);

  return OlympSelector;
}(React.Component);

var OlympFiles = function (_React$Component6) {
  _inherits(OlympFiles, _React$Component6);

  function OlympFiles() {
    _classCallCheck(this, OlympFiles);

    return _possibleConstructorReturn(this, (OlympFiles.__proto__ || Object.getPrototypeOf(OlympFiles)).apply(this, arguments));
  }

  _createClass(OlympFiles, [{
    key: "render",
    value: function render() {
      var tours = [];
      var grades = [];
      this.props.events.map(function (event) {
        event.files.map(function (file) {
          if (!tours.includes(file.tour)) {
            tours.push(file.tour);
          }
          if (!grades.includes(file.grade)) {
            grades.push(file.grade);
          }
        });
      });
      grades.sort(function (a, b) {
        return b - a;
      });
      return React.createElement(
        "div",
        { className: "d-flex flex-column justify-content-center align-items-center" },
        React.createElement(OlympSelector, { type: this.props.type, tour_options: tours, grade_options: grades, events: this.props.events })
      );
    }
  }]);

  return OlympFiles;
}(React.Component);
//Type of olympiad ('national', 'regional',...)


olymp_files = document.getElementById('olymp-files');
var olymp_type = olymp_files.dataset.olymp_type;
var static_location = olymp_files.dataset.static_location;

fetch("/olympiads_api/" + olymp_type + "/" + static_location).then(function (response) {
  return response.json();
}).then(function (olymp_events) {
  ReactDOM.render(React.createElement(OlympFiles, { events: olymp_events, type: olymp_type }), olymp_files);
});