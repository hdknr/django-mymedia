var apiMixin = {
  methods: {
    getEndpoint(base_url, instance){
      return (instance.id) ? base_url+ instance.id + '/' : base_url;
    },
    sendObject(base_url, instance){
      var endpoint = this.getEndpoint(base_url, instance);
      var config = {};
      axios.defaults.xsrfCookieName = 'csrftoken';
      axios.defaults.xsrfHeaderName = 'X-CSRFToken';
      var method = instance.id ? 'patch': 'post';
      return axios[method](endpoint, instance, config);
    },
    sendForm(endpoint, method, formData){
        var config = {headers: {'content-type': 'multipart/form-data'}};
        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        return axios[method](endpoint, formData, config);
    },
    sendMediaFile(id, formdata){
      var endpoint = "{% url 'mymedia_api:imagefile-list' %}";
      var method = 'put';
      if(id){
          method = 'patch';
          endpoint = "{% url 'mymedia_api:imagefile-detail' pk='___' %}".replace('___', id);
      }
      return this.sendForm(endpoint, method, formdata);
    },
    sendThumbnail(id, formdata){
      var endpoint = "{% url 'mymedia_api:thumbnail-list' %}";
      var method = 'put';
      if(id){
          method = 'patch';
          endpoint = "{% url 'mymedia_api:thumbnail-detail' pk='___' %}".replace('___', id);
      }
      return this.sendForm(endpoint, method, formdata);
    }
  } {# methods #}
}   {# apiMixin #}
