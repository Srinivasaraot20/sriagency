/* 
  Sri Ranganatha Agency (SRA) - Custom Interactive Scripts
*/

document.addEventListener('DOMContentLoaded', () => {
  // Sticky glassmorphism header on scroll
  const header = document.querySelector('.main-header');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });

  // Mobile menu hamburger toggle
  const hamburger = document.querySelector('.hamburger');
  const navMenu = document.querySelector('.nav-menu');

  if (hamburger && navMenu) {
    hamburger.addEventListener('click', () => {
      navMenu.classList.toggle('open');
      const isOpen = navMenu.classList.contains('open');
      hamburger.setAttribute('aria-expanded', isOpen);
    });

    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Navigation Login Button redirection to dedicated login page
  const loginBtns = document.querySelectorAll('.btn-login');
  loginBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      window.location.href = 'login.html';
    });
  });

  // Password Visibility Toggle Logic for dedicated login page
  const passwordInput = document.querySelector('#loginPassword');
  const passwordToggleBtn = document.querySelector('#passwordToggle');

  if (passwordInput && passwordToggleBtn) {
    passwordToggleBtn.addEventListener('click', () => {
      const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
      passwordInput.setAttribute('type', type);
      
      // Update eye icon state (open vs slashed)
      if (type === 'text') {
        // Eye Slashed Icon
        passwordToggleBtn.innerHTML = `
          <svg viewBox="0 0 24 24" style="width:100%; height:100%; fill:currentColor;">
            <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.04 2.63 3.01 4.79 5.58 6.01L4.99 19.6l1.41 1.41 15.6-15.6-1.41-1.41-2.6 2.6C16.32 5.37 14.28 4.5 12 4.5zm0 3c.8 0 1.55.22 2.2.6l-1.92 1.92c-.09-.01-.18-.02-.28-.02-1.66 0-3 1.34-3 3 0 .1.01.19.02.28L7.1 15.2c-.38-.65-.6-1.4-.6-2.2 0-2.76 2.24-5 5-5zm0 9c-1.52 0-2.93-.38-4.2-1.01l1.64-1.64c.73.55 1.63.85 2.56.85 2.21 0 4-1.79 4-4 0-.93-.3-1.83-.85-2.56l1.64-1.64c.63 1.27 1.01 2.68 1.01 4.2 0 4.39-4.27 7.5-9 7.5z"/>
          </svg>
        `;
      } else {
        // Eye Open Icon
        passwordToggleBtn.innerHTML = `
          <svg viewBox="0 0 24 24" style="width:100%; height:100%; fill:currentColor;">
            <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
          </svg>
        `;
      }
    });
  }

  // Login page form submission
  const loginPageForm = document.querySelector('#loginPageForm');
  if (loginPageForm) {
    loginPageForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = document.querySelector('#loginEmail').value;
      alert(`Welcome back to Sri Ranganatha Agency portal! Logged in as: ${email}`);
      window.location.href = 'index.html'; // Redirect to home page on login success
    });
  }

  // Slider / Carousel System Initialization
  initSlider('.categories-slider-wrapper', 4, 3, 2, 1);
  initSlider('.split-products-slider-wrapper', 3, 2, 2, 1);
  initSlider('.testimonials-slider-wrapper', 3, 2, 1, 1, true); // With dot indicators
  initSlider('.brands-slider-wrapper', 6, 4, 3, 2);

  // General carousel slider helper
  function initSlider(wrapperSelector, desktopSlides, laptopSlides, tabletSlides, mobileSlides, hasDots = false) {
    const wrapper = document.querySelector(wrapperSelector);
    if (!wrapper) return;

    const track = wrapper.querySelector('.slider-track');
    const prevBtn = wrapper.querySelector('.slider-btn-prev') || document.querySelector(`${wrapperSelector}-prev`);
    const nextBtn = wrapper.querySelector('.slider-btn-next') || document.querySelector(`${wrapperSelector}-next`);
    const slides = Array.from(track.children);
    
    let currentIndex = 0;
    let dotsContainer = null;

    if (hasDots) {
      dotsContainer = wrapper.querySelector('.slider-dots');
      createDots();
    }

    function getSlidesPerView() {
      const width = window.innerWidth;
      if (width > 1100) return desktopSlides;
      if (width > 768) return laptopSlides;
      if (width > 480) return tabletSlides;
      return mobileSlides;
    }

    function createDots() {
      if (!dotsContainer) return;
      dotsContainer.innerHTML = '';
      const slidesPerView = getSlidesPerView();
      const totalDots = Math.max(1, slides.length - slidesPerView + 1);

      for (let i = 0; i < totalDots; i++) {
        const dot = document.createElement('div');
        dot.classList.add('dot');
        if (i === 0) dot.classList.add('active');
        dot.addEventListener('click', () => {
          currentIndex = i;
          updateSlider();
        });
        dotsContainer.appendChild(dot);
      }
    }

    function updateSlider() {
      const slidesPerView = getSlidesPerView();
      const maxIndex = Math.max(0, slides.length - slidesPerView);
      
      if (currentIndex > maxIndex) currentIndex = maxIndex;
      if (currentIndex < 0) currentIndex = 0;

      const slideWidth = 100 / slidesPerView;
      slides.forEach(slide => {
        slide.style.flex = `0 0 ${slideWidth}%`;
        slide.style.maxWidth = `${slideWidth}%`;
      });

      const translateAmount = currentIndex * slideWidth;
      track.style.transform = `translateX(-${translateAmount}%)`;

      // Update button states
      if (prevBtn) {
        if (currentIndex === 0) prevBtn.classList.add('disabled');
        else prevBtn.classList.remove('disabled');
      }

      if (nextBtn) {
        if (currentIndex >= maxIndex) nextBtn.classList.add('disabled');
        else nextBtn.classList.remove('disabled');
      }

      // Update dots active status
      if (dotsContainer) {
        const dots = Array.from(dotsContainer.children);
        dots.forEach((dot, idx) => {
          if (idx === currentIndex) dot.classList.add('active');
          else dot.classList.remove('active');
        });
      }
    }

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        currentIndex--;
        updateSlider();
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        currentIndex++;
        updateSlider();
      });
    }

    // Update on resize
    window.addEventListener('resize', () => {
      if (hasDots) {
        createDots();
      }
      updateSlider();
    });

    updateSlider();
  }

  // Newsletter forms submission handling
  const newsletterForms = document.querySelectorAll('.newsletter-form, .footer-newsletter-form');
  newsletterForms.forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const emailInput = form.querySelector('input[type="email"]');
      if (emailInput && emailInput.value.trim() !== '') {
        alert(`Thank you! You have successfully subscribed to SRA updates with: ${emailInput.value}`);
        emailInput.value = '';
      }
    });
  });

  // View details on products triggers contact message
  const viewDetailsBtns = document.querySelectorAll('.product-link');
  viewDetailsBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      const productCard = e.target.closest('.product-card');
      const title = productCard.querySelector('.product-title').innerText;
      const category = productCard.querySelector('.product-cat').innerText;
      const text = `Hello Sri Ranganatha Agency, I am interested in inquiring about "${title}" (${category}). Please provide me details.`;
      
      const whatsappUrl = `https://wa.me/919515515557?text=${encodeURIComponent(text)}`;
      window.open(whatsappUrl, '_blank');
    });
  });

  // Pre-fetch IP address
  let userIp = "127.0.0.1";
  fetch('https://api.ipify.org?format=json')
    .then(res => res.json())
    .then(data => { userIp = data.ip; })
    .catch(() => { /* Fallback to default */ });

  // Contact Form Submission Handling
  const contactForm = document.querySelector('#contactForm');
  const successModal = document.querySelector('#successModal');
  const btnContinueBrowsing = document.querySelector('#btnContinueBrowsing');
  const btnModalWhatsapp = document.querySelector('#btnModalWhatsapp');

  if (contactForm && successModal) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();

      // Field Values
      const name = document.querySelector('#contactName').value.trim();
      const phone = document.querySelector('#contactPhone').value.trim();
      const email = document.querySelector('#contactEmail').value.trim();
      const location = document.querySelector('#contactLocation').value.trim();
      const crop = document.querySelector('#contactCrop').value;
      const category = document.querySelector('#contactCategory').value;
      const subject = document.querySelector('#contactSubject').value.trim();
      const message = document.querySelector('#contactMessage').value.trim();

      // Basic Validation
      if (!name || !phone || !message) {
        alert("Please fill in all required fields.");
        return;
      }

      // Format Date & Time: "12 July 2026 10:35 AM"
      const now = new Date();
      const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
      const day = now.getDate();
      const month = months[now.getMonth()];
      const year = now.getFullYear();
      let hours = now.getHours();
      const minutes = String(now.getMinutes()).padStart(2, '0');
      const ampm = hours >= 12 ? 'PM' : 'AM';
      hours = hours % 12;
      hours = hours ? hours : 12; // the hour '0' should be '12'
      const formattedDate = `${day} ${month} ${year}\n${hours}:${minutes} ${ampm}`;

      // Save to localStorage (Simulating Database)
      const enquiries = JSON.parse(localStorage.getItem('enquiries') || '[]');
      const newEnquiry = {
        name,
        phone,
        email: email || "Not provided",
        village: location || "Not provided",
        crop: crop || "Not provided",
        productCategory: category || "Not provided",
        subject: subject || "Not provided",
        message,
        dateTime: formattedDate.replace('\n', ' '),
        ipAddress: userIp,
        browserInfo: navigator.userAgent,
        status: "New"
      };
      enquiries.push(newEnquiry);
      localStorage.setItem('enquiries', JSON.stringify(enquiries));

      // Construct WhatsApp Message
      const waMessage = `🌱 *New Farmer Enquiry*

👤 *Name:*
${name}

📞 *Phone:*
${phone}

📧 *Email:*
${email || 'Not provided'}

🏡 *Village:*
${location || 'Not provided'}

🌾 *Crop:*
${crop || 'Not provided'}

🧪 *Product Category:*
${category || 'Not provided'}

📝 *Subject:*
${subject || 'Not provided'}

💬 *Message:*
${message}

🕒 *Date:*
${formattedDate}

🌐 *Website:*
https://sriagency.in`;

      const whatsappUrl = `https://wa.me/919515515557?text=${encodeURIComponent(waMessage)}`;

      // Try opening WhatsApp immediately
      window.open(whatsappUrl, '_blank');

      // Update link inside the modal just in case popups are blocked or user manually clicks
      if (btnModalWhatsapp) {
        btnModalWhatsapp.href = whatsappUrl;
      }

      // Show Success Modal
      successModal.style.display = 'flex';
      successModal.classList.add('open');
    });

    // Close Modal and reset form when Continue Browsing is clicked
    if (btnContinueBrowsing) {
      btnContinueBrowsing.addEventListener('click', () => {
        successModal.style.display = 'none';
        successModal.classList.remove('open');
        contactForm.reset();
      });
    }
  }
});

// ==========================================================================
// PRODUCT DETAILS MODAL HANDLING
// ==========================================================================
const productData = {
  urea: {
    title: 'Urea 46%',
    badge: 'Fertiliser',
    badgeClass: 'badge-fertiliser',
    subtitle: 'Nitrogen Fertilizer',
    img: 'static/assets/urea_bag.jpg',
    brand: 'IFFCO',
    technical: 'Nitrogen 46%',
    mode: 'Provides essential Nitrogen directly to plants to enhance vegetative growth and leaf development.',
    crops: 'Paddy, Wheat, Cotton, Sugarcane, Maize, Vegetables.',
    benefits: 'Promotes lush green growth, increases photosynthesis, and significantly boosts crop yield.',
    category: 'Fertilizers'
  },
  dap: {
    title: 'DAP 18-46-0',
    badge: 'Fertiliser',
    badgeClass: 'badge-fertiliser',
    subtitle: 'Phosphorus Fertilizer',
    img: 'static/assets/dap_bag.jpg',
    brand: 'Coromandel / IFFCO',
    technical: 'Di-Ammonium Phosphate (N: 18%, P: 46%)',
    mode: 'Provides essential phosphate at root zones to stimulate strong root growth and early plant establishment.',
    crops: 'Paddy, Cotton, Groundnut, Pulses, Chillies, Vegetables.',
    benefits: 'Enhances early root development, promotes strong flowering/fruiting, and improves crop resilience.',
    category: 'Fertilizers'
  },
  emamectin: {
    title: 'Emamectin 5% SG',
    badge: 'Insecticide',
    badgeClass: 'badge-insecticide',
    subtitle: 'Crop Protection Insecticide',
    img: 'static/assets/emamectin_bottle.jpg',
    brand: 'Syngenta / Bayer',
    technical: 'Emamectin Benzoate 5% SG',
    mode: 'Acts as contact and stomach insecticide, quickly paralyzing and stopping pests from feeding within hours.',
    crops: 'Cotton, Paddy, Chillies, Grapes, Vegetables, Pulses.',
    benefits: 'Provides highly effective control of bollworms, fruit borers, caterpillars, pod borers, and thrips.',
    category: 'Pesticides'
  },
  caltan: {
    title: 'Caltan',
    badge: 'Fungicide',
    badgeClass: 'badge-fungicide',
    subtitle: 'Crop Protection Fungicide',
    img: 'static/assets/caltan_bottle.jpg',
    brand: 'UPL',
    technical: 'Hexaconazole 5% SC / Caltan Formula',
    mode: 'Systemic fungicide that penetrates plant tissue, offering both protective and curative action against fungus spores.',
    crops: 'Paddy, Groundnut, Mango, Grapes, Chillies, Vegetables.',
    benefits: 'Delivers outstanding control over sheath blight, powdery mildew, rust, leaf spots, and rice blast.',
    category: 'Pesticides'
  },
  herbicide_24d: {
    title: '2,4-D',
    badge: 'Herbicide',
    badgeClass: 'badge-herbicide',
    subtitle: 'Crop Protection Herbicide',
    img: 'static/assets/herbicide_24d_bottle.jpg',
    brand: 'Heranba',
    technical: '2,4-D Ethyl Ester / Sodium Salt',
    mode: 'Selective systemic herbicide absorbed by foliage and roots, disrupting weed growth without affecting target cereal crops.',
    crops: 'Paddy, Sugarcane, Wheat, Maize.',
    benefits: 'Controls broadleaf weeds, annual weeds, and sedges in paddy fields and sugarcane plantations.',
    category: 'Pesticides'
  }
};

function showProductDetails(id) {
  const product = (window.djangoProductData && window.djangoProductData[id]) || productData[id];
  if (!product) return;

  const modalImg = document.getElementById('modalProductImg');
  const modalBadge = document.getElementById('modalProductBadge');
  const modalTitle = document.getElementById('modalProductTitle');
  const modalSub = document.getElementById('modalProductSub');
  const modalBrand = document.getElementById('modalProductBrand');
  const modalTechnical = document.getElementById('modalProductTechnical');
  const modalMode = document.getElementById('modalProductMode');
  const modalCrops = document.getElementById('modalProductCrops');
  const modalBenefits = document.getElementById('modalProductBenefits');
  const modalWhatsAppBtn = document.getElementById('modalWhatsAppBtn');
  const modalContactBtn = document.getElementById('modalContactBtn');

  if (modalImg) {
    modalImg.src = product.img;
    modalImg.alt = product.title;
  }
  if (modalBadge) {
    modalBadge.textContent = product.badge;
    modalBadge.className = 'top-product-badge ' + product.badgeClass;
  }
  if (modalTitle) modalTitle.textContent = product.title;
  if (modalSub) modalSub.textContent = product.subtitle;
  if (modalBrand) modalBrand.textContent = product.brand;
  if (modalTechnical) modalTechnical.textContent = product.technical;
  if (modalMode) modalMode.textContent = product.mode;
  if (modalCrops) modalCrops.textContent = product.crops;
  if (modalBenefits) modalBenefits.textContent = product.benefits;

  // Set WhatsApp CTA Link
  if (modalWhatsAppBtn) {
    const waMsg = `Hello Sri Ranganatha Agency, I would like to enquire about the product: *${product.title}* (${product.subtitle}). Please share pricing and availability.`;
    modalWhatsAppBtn.href = `https://wa.me/919515515557?text=${encodeURIComponent(waMsg)}`;
  }
  
  // Set Contact form prefill link
  if (modalContactBtn) {
    modalContactBtn.href = `contact.html?subject=Inquiry about ${encodeURIComponent(product.title)}&category=${encodeURIComponent(product.category)}`;
  }

  // Open modal
  const modal = document.getElementById('productModal');
  if (modal) {
    modal.style.display = 'flex';
  }
}

function closeProductModal() {
  const modal = document.getElementById('productModal');
  if (modal) {
    modal.style.display = 'none';
  }
}

// Close product modal if clicked outside
window.addEventListener('click', function(e) {
  const modal = document.getElementById('productModal');
  if (modal && e.target === modal) {
    closeProductModal();
  }
});



