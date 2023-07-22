console.log("hello")
function copyToClipboard(text) {
  const textarea = document.createElement('textarea');
  textarea.value = text;
  textarea.style.position = 'fixed'; // Ensure the textarea is always visible
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand('copy');
  document.body.removeChild(textarea);
}




var layerCount = 1;
var attributes_and_rarities_indexing = 1;
var images_counter = 1; 

var temporary_data_holder = [];

function display_sample_image(){
  var z_index_fix_value = 999;
    var total_generated_nft = 1;
    $(".nft-sample").empty();
    $(".total-nfts").empty();
    var all_files = document.querySelectorAll('.layer-image-selector');
    var filesArray = Array.from(all_files);
    
    filesArray.sort(function(a, b) {
      var layerA = parseInt(a.getAttribute('data-layer'));
      var layerB = parseInt(b.getAttribute('data-layer'));
    
      return layerA - layerB;
    });

    // The filesArray variable is now sorted based on the data-layer attribute
    console.log(filesArray);
    for (var j = 0; j < filesArray.length; j++) {

      var files = filesArray[j].files;
      if (files.length > 0) {
        total_generated_nft *= files.length;
      }
    
      if (files.length > 0) {
        const reader = new FileReader();
        reader.addEventListener('load', function() {
          const sample_nft_image = new Image();
          sample_nft_image.src = reader.result;
          sample_nft_image.style.backgroundColor = 'transparent';
          z_index_fix_value += 1;
          console.log(z_index_fix_value);
          sample_nft_image.style.zIndex = z_index_fix_value;
          $(".nft-sample").append(sample_nft_image);
        });
        reader.readAsDataURL(files[Math.floor(Math.random() * files.length)]);
      }
    }

  if(total_generated_nft > 1){
    $(".total-nfts").append("<h6 class='text-white'>Possible NFTs: " + total_generated_nft + "</h6>")
  }

// setInterval(display_sample_image, 10000);

  
}

function updateLayerButtons() {
  $('.remove-layer').prop('disabled', $('#layers .layer').length === 1);
}

$('#add-layer').click(function() {
  layerCount++;
  var newLayer = '<div class="layer">';
  newLayer += '<div class="input-group mb-3">';
  newLayer += '<span class="input-group-text custom-input-group-text">Layer Name</span>';
  newLayer += '<div class="form-row"><div class="col-12"><input type="text" class="form-control layer-name custom-input" required value="Layer ' + layerCount + '"></div></div>';
  newLayer += '<button type="button" class="btn btn-danger remove-layer custom-button">X</button>';
  newLayer += '</div>';
  newLayer += '<div class="image-selector mb-3">';
  newLayer += '<div class="layer-image-preview row" style="position: relative" data-layer="' + layerCount + '"><div class="col-md-1 align-self-center"><input type="file" required class="form-control-file layer-image-selector custom-file" data-layer="' + layerCount + '" multiple></div></div>';
  newLayer += '</div>';
  newLayer += '</div>';
  $('#layers').append(newLayer);
  updateLayerButtons();
});

$(document).on('click', '.remove-layer', function() {
  var layerNumber = $(this).closest(".layer").find(".layer-image-preview").data("layer");
  temporary_data_holder = temporary_data_holder.filter(function(element) {
    return element.id !== layerNumber;
  });
  console.log("Data-layer attribute value: " + layerNumber);
  $(this).closest('.layer').remove();
  display_sample_image();
//   updateLayerButtons();
});

// setInterval(display_sample_image, 10000);

$(document).on('change', '.layer-image-selector', function() {
  var input = $(this)[0];
  var layer = $(this).closest('.layer').find('.layer-name');
  var layerNumber = $(this).closest(".layer").find(".layer-image-preview").data("layer");
  temporary_data_holder = temporary_data_holder.filter(function(element) {
    return element.id !== layerNumber;
  });
  console.log("Data-layer attribute value: " + layerNumber);
  if (input.files && input.files.length) {
    var layerIndex = $(input).data('layer');
    $('.layer-image-preview[data-layer="' + layerIndex + '"] .image-container').remove();
    var rarity_estimated = 100 / input.files.length;
    if (!Number.isInteger(rarity_estimated)) {
        rarity_estimated =  Math.floor(rarity_estimated);
    }
    var temp_meta_data = []
    for (var i = 0; i < input.files.length; i++) {
      var reader = new FileReader();
      // console.log(input.files[i].name);
      reader.onload = (function(file) {
        return function(e) {
            var img = $('<img class="img-thumbnail">').attr('src', e.target.result);
            var closeButton = $('<button>').attr('type', 'button').addClass('btn-close rmv-btn-style').attr('aria-label', 'Close').click(function() {
                $(this).closest('.image-container').remove();
            });
            temp_meta_data.push({"file": file, "attribute_id": "attribute" +images_counter, "rarity_id": "rarity"+images_counter});
            var fileName = file.name;
            fileName = fileName.split(".");
            fileName.pop();
            fileName =  fileName.join('.');

            // for check if rarirt already mentioned in file name
            var is_rarity_exist = fileName.split("-");
            if (is_rarity_exist.length > 1){
              rarity_estimated = is_rarity_exist[0];
            }
            // var imageContainer = $('<div style="position: relative">').addClass('image-container col-md-1').append(img, closeButton);
            var imageContainer = $('<div style="position: relative">').addClass('image-container col-md-1').append(`<input type="number" class="rarity form-control" value="`+rarity_estimated+`"" required id="rarity`+images_counter+`"" placeholder="rarity %"/>`, img, `<input type="text" required class="attribute form-control"  id="attribute`+images_counter+`"  value="`+fileName+`"" placeholder="Attribute"/>`);
            $('.layer-image-preview[data-layer="' + layerIndex + '"]').prepend(imageContainer);
            images_counter ++;
        };
      })(input.files[i]);
      reader.readAsDataURL(input.files[i]);
    }
    temporary_data_holder.push({"id": layerNumber, "layer": layer, "meta_data": temp_meta_data});
    console.dir(temporary_data_holder);
  }


  display_sample_image();


});

$(document).on('input', '.layer-name', function() {
  var layerIndex = $(this).closest('.layer').index() + 1;
  $('.layer-image-selector[data-layer="' + layerIndex + '"]').attr('title', $(this).val() + ' Image Selector');
});

// initialize the first layer
$('.layer-image-selector[data-layer="1"]').attr('title', $('.layer-name').val() + ' Image Selector');



const form = document.getElementById("layersForm");

form.addEventListener("submit", (e) => {
    e.preventDefault(); // prevent default form submission

    // validate required fields
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    var formData = new FormData();
    var data = [];
    var layer_order = 0;
    temporary_data_holder.forEach(function(v) {
      var layerName = v.layer.val();
      v.meta_data.forEach(function(md, index) {
        console.log(index);
        if (index === 0){
            formData.append("layer" + layer_order, layerName);
        }
        var fle = md.file;
        var rarity = $("#" + md.rarity_id).val();
        var attribute = $("#" + md.attribute_id).val();
        formData.append("lay_img" + layer_order + index, fle);
        formData.append("lay_rarity" + layer_order + index, rarity);
        formData.append("lay_attribute" + layer_order + index, attribute); 
        console.log(md.file, rarity, attribute);
      })
      layer_order ++;
    });

  var progressBar = $('.progress-bar');
  var splash = $('#splash');
  var content = $('#content');
  splash.show();
$.ajax({
          url: upload_layers,
          // url: "http://194.233.67.87/upload-layers/",
          type: 'POST',
          data: formData,
          processData: false,
          contentType: false,
          xhr: function() {
            var xhr = new window.XMLHttpRequest();
            var chunkSize = 5 * 1024 * 1024; // 5MB in bytes
            xhr.upload.addEventListener('progress', function(evt) {
              if (evt.lengthComputable) {
                var percentComplete = evt.loaded / evt.total;
                progressBar.css('width', percentComplete * 100 + '%');
              }
            }, false);
            return xhr;
          },
          success: function(response) {
            if (response.success) {

              // response = JSON.parse(data);
              console.log(response);
              if(response.success){
                  console.log(response);
                  $("#nftsPaths_input").val(response.input);
                  $("#nftsPaths_output").val(response.output);
                  $("#task_id").val(response.task_id);
                  $("#layersForm").hide();
                  $(".form-1-btn").hide();
                  $("#gennft-form").show();
              }
              // window.location.reload();
              splash.hide();
              // content.show();
            } else {
              // alert('File upload failed:\n' + response.errors);
              console.log(response);
              splash.hide();
              // content.show();
            }
          },
          error: function(xhr, status, error) {
            alert('File upload failed: ' + error);
            splash.hide();
            // content.show();
          }
        });

// ------------------




});


var splash = $('#splash');
var content = $('#content');

var is_resources_ready = false;
    
    $('#gennft-form').on('submit', function(event) {
        event.preventDefault();
        var form_data = $(this).serialize();
        var progressBar = $('.progress-bar');
        splash.show();
        content.hide();
        $.ajax({
            url:generate_nfts_layer,
            // url: "http://194.233.67.87/generate-nfts-layers",
            type: 'POST',
            data: form_data,
            processData: false,
            xhr: function() {
              var xhr = new window.XMLHttpRequest();
              xhr.upload.addEventListener('progress', function(evt) {
                if (evt.lengthComputable) {
                  var percentComplete = evt.loaded / evt.total;
                  progressBar.css('width', percentComplete * 100 + '%');
                }
              }, false);
              return xhr;
            },
            success: function(response) {

                console.log(response);
                if(response.valid){
                  // check_status(response.task_id);
                  // is_resources_ready = 1;
                  check_status();
                  console.log("---------");
                  console.log('Task started successfully');
                  console.log(response);
                  console.log("---------");

                }
                else{
                  alert(response);
                  // is_resources_ready = 0;
                }
                // splash.hide();
                // content.show();
            },
            error: function(xhr, status, error) {
                // is_resources_ready = 0;
                alert('Error starting task');
                // splash.hide();
                // content.show();
            }
        });
    });

    function check_status(){
      var progressBar = $('.progress-bar');
      var path = $("#nftsPaths_output").val();
      var task_id = $("#task_id").val();
      var total_to_generate = $("#id_totalnfts").val();
      // $.post("http://194.233.67.87/get_details/", {output_path: path, "task_id": task_id})
      // $.post("/get_details/", {output_path: path, "task_id": task_id})
      $.post(getDetailsUrl, {output_path: path, "task_id": task_id})
      .done(function(data) {
          console.log(data);
          if(data.valid){
            console.log("Images Generated: ", data.count);
            if(data.status == "completed"){
              console.log("Completed");
              is_resources_ready = 1;
              $(".form-hideable").hide();
              $("#home-link").show();
              $("#path").val(path);
              $("#download-btn").show();
              $("#uploadipfs-btn").show();

              splash.hide();
              content.show();
              // location.reload();

            }
            else if(data.status == "running" || data.status == "created"){
              var percentComplete = 0 / total_to_generate;
                progressBar.css('width', percentComplete * 100 + '%');
              setTimeout(check_status, 3000);

            }
            else if(data.status == "error"){
              splash.hide();
              content.show();
              console.log(data.msg);

            }
            var percentComplete = data.count / total_to_generate;
            progressBar.css('width', percentComplete * 100 + '%');

          }
          else{
            console.log(data.error);
            setTimeout(check_status, 3000);
          }
        })
        .fail(function(xhr, status, error) {
          alert(xhr.responseText);

        });
        
    }


// for ipfs uploading code

    
$('#uploadipfs-btn').on('click', function(event) {
        // event.preventDefault();
        is_resources_ready = false;
        var progressBar = $('.progress-bar');
        var path = $("#nftsPaths_input").val();
        var task_id = $("#task_id").val();
        var splash = $('#splash');
        var content = $('#content');
        check_status_ipsfs_upload();
        splash.show();
        content.hide();

        $.ajax({
          url:upload_ipfs_server,
            // url:"http://194.233.67.87/upload-ipfs-server/",
            type: 'POST',
            data: {resources: path, task_id: task_id},
            xhr: function() {
              var xhr = new window.XMLHttpRequest();
              xhr.upload.addEventListener('progress', function(evt) {
                if (evt.lengthComputable) {
                  var percentComplete = evt.loaded / evt.total;
                  progressBar.css('width', percentComplete * 100 + '%');
                }
              }, false);
              return xhr;
            },
            success: function(response) {
                console.log('Task started uploading successfully');
                console.log(response);
                if(response.valid){
                  // check_status(response.task_id);
                  // is_resources_ready = 1;
                  // $("#ipfsdownload-btn").show();
                  console.log("----ipfs-----");
                  console.log(response);
                  console.log("----/ipfs-----");

                }
                else{
                  console.log("error upload ipfs");
                  console.log(response);
                  is_resources_ready = 0;
                }
                // splash.hide();
                // content.show();
            },
            error: function(xhr, status, error) {
                console.log(xhr);
                is_resources_ready = 0;
                alert('Error starting task');
                splash.hide();
                content.show();
            }
        });
    });

    function check_status_ipsfs_upload(){
      var progressBar = $('.progress-bar');
      var path = $("#nftsPaths_output").val();
      var task_id = $("#task_id").val();
      var total_to_generate = $("#id_totalnfts").val();
      // $.post("http://194.233.67.87/get_details/", {output_path: path, "task_id": task_id})
      $.post(getDetailsUrl, {output_path: path, "task_id": task_id})
        .done(function(data) {
          console.log(data);
          if(data.valid){
            console.log("Images Generated: ", data.count);
            if(data.status == "uploaded"){
              splash.hide();
              content.show();
              console.log("Completed");
              $(".form-hideable").hide();
              $("#home-link").show();
                  // Show pop-up with the cid value
              var cid = data.cid;
              var popupContent = 'CID: ' + cid;
              // Use SweetAlert to display the pop-up message
              Swal.fire({
                title: 'CID',
                text: popupContent,
                icon: 'info',
                showCancelButton: true,
                cancelButtonText: 'Close',
                confirmButtonText: 'Copy CID',
                allowOutsideClick: false,
                didOpen: () => {
                  const copyButton = Swal.getConfirmButton();
                  copyButton.addEventListener('click', () => {
                    copyToClipboard(cid);
                    Swal.fire('Copied!', 'The CID has been copied to the clipboard.', 'success');
                  });
                }
                });
                                                    

            }
            else if(data.status == "uploading" || data.status == "completed"){
              setTimeout(check_status_ipsfs_upload, 3000);

            }
            else if(data.status == "error"){
              alert("Error");
              console.log(data.msg);
            }

          }
          else{
            console.log("else error");

            console.log(data);
            setTimeout(check_status_ipsfs_upload, 3000);
          }
        })
        .fail(function(xhr, status, error) {
          console.log("faillll");
          console.log(xhr.responseText);
          
        });
        
    }
