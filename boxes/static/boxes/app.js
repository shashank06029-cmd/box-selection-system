const productSelect = document.getElementById("product");
const quantityInput = document.getElementById("quantity");
const addProductButton = document.getElementById("add-product");

const orderItemsContainer = document.getElementById("order-items");
const orderContainer = document.getElementById("order-container");
const emptyState = document.getElementById("empty-state");

const recommendButton = document.getElementById("recommend-button");
const itemCount = document.getElementById("item-count");

const formError = document.getElementById("form-error");

const resultSection = document.getElementById("result-section");
const successResult = document.getElementById("success-result");
const failureResult = document.getElementById("failure-result");

const boxName = document.getElementById("box-name");
const boxCost = document.getElementById("box-cost");
const boxWeight = document.getElementById("box-weight");
const boxId = document.getElementById("box-id");
const orderWeight = document.getElementById("order-weight");

const failureMessage = document.getElementById("failure-message");
const failureWeight = document.getElementById("failure-weight");

const csrfToken = document.querySelector(
    "[name=csrfmiddlewaretoken]"
).value;

let products = [];
let orderItems = [];


async function loadProducts() {
    try {
        const response = await fetch("/api/products/");

        if (!response.ok) {
            throw new Error("Unable to load products.");
        }

        products = await response.json();

        productSelect.innerHTML = `
            <option value="">Select a product</option>
        `;

        products.forEach((product) => {
            const option = document.createElement("option");

            option.value = product.id;
            option.textContent = product.name;

            productSelect.appendChild(option);
        });

        if (products.length === 0) {
            showFormError(
                "No products available. Add products from Admin Panel."
            );
        }
    } catch (error) {
        showFormError(
            "Unable to load products. Please check the server."
        );
    }
}


function addProduct() {
    clearFormError();

    const productId = Number(productSelect.value);
    const quantity = Number(quantityInput.value);

    if (!productId) {
        showFormError("Please select a product.");
        return;
    }

    if (!quantity || quantity < 1) {
        showFormError("Quantity must be at least 1.");
        return;
    }

    const product = products.find(
        (item) => item.id === productId
    );

    if (!product) {
        showFormError("Selected product was not found.");
        return;
    }

    const existingItem = orderItems.find(
        (item) => item.product === productId
    );

    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        orderItems.push({
            product: productId,
            name: product.name,
            length: Number(product.length),
            width: Number(product.width),
            height: Number(product.height),
            weight: Number(product.weight),
            quantity
        });
    }

    productSelect.value = "";
    quantityInput.value = 1;

    renderOrderItems();
}


function renderOrderItems() {
    orderItemsContainer.innerHTML = "";

    if (orderItems.length === 0) {
        emptyState.classList.remove("hidden");
        orderContainer.classList.add("hidden");
        recommendButton.disabled = true;
        itemCount.textContent = "0 items";
        return;
    }

    emptyState.classList.add("hidden");
    orderContainer.classList.remove("hidden");
    recommendButton.disabled = false;

    const totalQuantity = orderItems.reduce(
        (total, item) => total + item.quantity,
        0
    );

    itemCount.textContent =
        `${totalQuantity} ${totalQuantity === 1 ? "item" : "items"}`;

    orderItems.forEach((item, index) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>
                <span class="product-name">
                    ${escapeHtml(item.name)}
                </span>
            </td>

            <td>
                ${item.length} × ${item.width} × ${item.height}
            </td>

            <td>
                ${item.weight.toFixed(2)} kg
            </td>

            <td>
                ${item.quantity}
            </td>

            <td>
                <button
                    class="remove-button"
                    data-index="${index}"
                    type="button"
                >
                    Remove
                </button>
            </td>
        `;

        orderItemsContainer.appendChild(row);
    });

    document.querySelectorAll(".remove-button").forEach((button) => {
        button.addEventListener("click", () => {
            const index = Number(button.dataset.index);

            orderItems.splice(index, 1);

            renderOrderItems();
        });
    });
}


async function recommendBox() {
    if (orderItems.length === 0) {
        return;
    }

    recommendButton.disabled = true;
    recommendButton.textContent = "Checking...";

    resultSection.classList.add("hidden");
    successResult.classList.add("hidden");
    failureResult.classList.add("hidden");

    try {
        const response = await fetch("/api/recommend-box/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                items: orderItems.map((item) => ({
                    product: item.product,
                    quantity: item.quantity
                }))
            })
        });

        const data = await response.json();

        resultSection.classList.remove("hidden");

        if (data.success) {
            showSuccessResult(data);
        } else {
            showFailureResult(data);
        }

        resultSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    } catch (error) {
        resultSection.classList.remove("hidden");
        successResult.classList.add("hidden");
        failureResult.classList.remove("hidden");

        failureMessage.textContent =
            "Unable to connect to the recommendation service.";

        failureWeight.textContent =
            "Please check that the Django server is running.";
    } finally {
        recommendButton.disabled = false;
        recommendButton.textContent = "Recommend Box";
    }
}


function showSuccessResult(data) {
    successResult.classList.remove("hidden");
    failureResult.classList.add("hidden");

    boxName.textContent = data.recommended_box.name;

    boxCost.textContent =
        `₹${Number(data.recommended_box.cost).toFixed(2)}`;

    boxWeight.textContent =
        `${Number(data.recommended_box.max_weight).toFixed(2)} kg`;

    orderWeight.textContent =
        `${Number(data.total_weight).toFixed(2)} kg`;

    boxId.textContent = data.recommended_box.id;
}


function showFailureResult(data) {
    successResult.classList.add("hidden");
    failureResult.classList.remove("hidden");

    failureMessage.textContent =
        data.message || "No suitable box found.";

    failureWeight.textContent =
        `Order Weight: ${Number(data.total_weight || 0).toFixed(2)} kg`;
}


function showFormError(message) {
    formError.textContent = message;
    formError.classList.remove("hidden");
}


function clearFormError() {
    formError.textContent = "";
    formError.classList.add("hidden");
}


function escapeHtml(value) {
    const element = document.createElement("div");

    element.textContent = value;

    return element.innerHTML;
}


addProductButton.addEventListener("click", addProduct);

recommendButton.addEventListener("click", recommendBox);

quantityInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        addProduct();
    }
});

loadProducts();